#!/usr/bin/env python3
"""
Validate GIS pipeline against contract and emit manifest + report.
"""

import argparse
import json
import os
import sys
from datetime import datetime
from typing import Dict, List, Optional, Tuple

import psycopg2


def build_db_url(args: argparse.Namespace) -> str:
    if args.db_url:
        return args.db_url
    host = os.environ.get("DB_HOST", "localhost")
    port = os.environ.get("DB_PORT", "5432")
    db = os.environ.get("DB_NAME", "villa_canabrava")
    user = os.environ.get("DB_USER", "postgres")
    password = os.environ.get("DB_PASSWORD", "postgres")
    return f"postgresql://{user}:{password}@{host}:{port}/{db}"


def read_contract(path: str) -> dict:
    with open(path, "r", encoding="utf-8-sig") as handle:
        return json.load(handle)


def query_one(cur, sql: str, params=None):
    cur.execute(sql, params or ())
    return cur.fetchone()[0]


def query_rows(cur, sql: str, params=None):
    cur.execute(sql, params or ())
    return cur.fetchall()


def fetch_extent(cur, schema: str) -> Optional[Tuple[float, float, float, float]]:
    cur.execute(
        f"""
        SELECT
            ST_XMin(extent_geom),
            ST_YMin(extent_geom),
            ST_XMax(extent_geom),
            ST_YMax(extent_geom)
        FROM (
            SELECT ST_Extent(geometry)::geometry AS extent_geom
            FROM {schema}.geo_features
            WHERE geometry IS NOT NULL
        ) s
        """
    )
    row = cur.fetchone()
    if row and all(v is not None for v in row):
        return row[0], row[1], row[2], row[3]
    return None


def fetch_perimeter_stats(cur, schema: str) -> Tuple[Optional[str], Optional[float], Optional[float]]:
    candidates = query_rows(
        cur,
        f"SELECT DISTINCT layer_name FROM {schema}.geo_features WHERE layer_name ILIKE %s",
        ("%PERIMETRO%",),
    )
    if not candidates:
        return None, None, None

    best_layer = None
    best_area = None
    best_perimeter = None

    for (layer_name,) in candidates:
        cur.execute(
            f"""
            SELECT
                ST_Area(geom::geography) / 10000.0,
                ST_Perimeter(geom::geography) / 1000.0
            FROM (
                SELECT ST_UnaryUnion(ST_Collect(geometry)) AS geom
                FROM {schema}.geo_features
                WHERE layer_name = %s AND geometry IS NOT NULL
            ) s
            """,
            (layer_name,),
        )
        row = cur.fetchone()
        if not row or row[0] is None:
            continue
        area_ha, perimeter_km = float(row[0]), float(row[1])
        if best_area is None or area_ha > best_area:
            best_layer = layer_name
            best_area = area_ha
            best_perimeter = perimeter_km

    return best_layer, best_area, best_perimeter


def within_tolerance(value: float, expected: float, pct: float) -> bool:
    if expected == 0:
        return abs(value) <= pct
    return abs(value - expected) <= abs(expected) * (pct / 100.0)


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate pipeline contract")
    parser.add_argument("--db-url", default="", help="PostgreSQL connection URL")
    parser.add_argument("--schema", default="villa_canabrava", help="Target schema")
    parser.add_argument("--contract", required=True, help="Contract JSON path")
    parser.add_argument("--out-manifest", required=True, help="Manifest output path")
    parser.add_argument("--out-report", required=True, help="Report output path")
    parser.add_argument("--strict", action="store_true", help="Fail on duplicates")
    args = parser.parse_args()

    contract = read_contract(args.contract)
    expected_layers = int(contract.get("expected_layers", 0))
    bounds = contract.get("bounds", {})
    tolerances = contract.get("tolerances", {})
    tol_area = float(tolerances.get("area_ha_pct", 1.0))
    tol_perim = float(tolerances.get("perimeter_km_pct", 1.0))
    tol_bounds = float(tolerances.get("bounds_deg", 0.01))

    db_url = build_db_url(args)
    conn = psycopg2.connect(db_url)
    cur = conn.cursor()

    postgis_ok = query_one(cur, "SELECT EXISTS (SELECT 1 FROM pg_extension WHERE extname = 'postgis')")
    total_features = query_one(cur, f"SELECT COUNT(*) FROM {args.schema}.geo_features")
    layer_count = query_one(cur, f"SELECT COUNT(DISTINCT layer_name) FROM {args.schema}.geo_features")
    invalid = query_one(cur, f"SELECT COUNT(*) FROM {args.schema}.geo_features WHERE geometry IS NOT NULL AND NOT ST_IsValid(geometry)")
    srid_mismatch = query_one(cur, f"SELECT COUNT(*) FROM {args.schema}.geo_features WHERE geometry IS NOT NULL AND ST_SRID(geometry) <> 4326")

    duplicates = query_rows(
        cur,
        f"""
        SELECT layer_name, feature_hash, COUNT(*)
        FROM {args.schema}.geo_features
        WHERE feature_hash IS NOT NULL
        GROUP BY layer_name, feature_hash
        HAVING COUNT(*) > 1
        ORDER BY COUNT(*) DESC
        """,
    )

    extent = fetch_extent(cur, args.schema)
    perimeter_layer, area_ha, perimeter_km = fetch_perimeter_stats(cur, args.schema)

    cur.close()
    conn.close()

    status = "PASS"
    issues: List[str] = []

    if not postgis_ok:
        status = "FAIL"
        issues.append("PostGIS extension not installed")

    if expected_layers and layer_count != expected_layers:
        status = "FAIL"
        issues.append(f"Layer count mismatch: {layer_count} (expected {expected_layers})")

    if invalid > 0:
        status = "FAIL"
        issues.append(f"Invalid geometries: {invalid}")

    if srid_mismatch > 0:
        status = "FAIL"
        issues.append(f"SRID mismatch: {srid_mismatch}")

    if duplicates:
        issues.append(f"Duplicate geometries: {len(duplicates)}")
        if args.strict:
            status = "FAIL"

    if extent:
        min_lon, min_lat, max_lon, max_lat = extent
        expected_min_lon = float(bounds.get("lon_min", min_lon))
        expected_max_lon = float(bounds.get("lon_max", max_lon))
        expected_min_lat = float(bounds.get("lat_min", min_lat))
        expected_max_lat = float(bounds.get("lat_max", max_lat))

        bounds_ok = (
            min_lon >= expected_min_lon - tol_bounds
            and max_lon <= expected_max_lon + tol_bounds
            and min_lat >= expected_min_lat - tol_bounds
            and max_lat <= expected_max_lat + tol_bounds
        )
        if not bounds_ok:
            status = "FAIL"
            issues.append("Extent outside contract bounds")

    if area_ha is not None and perimeter_km is not None:
        expected_area = float(contract.get("area_ha", area_ha))
        expected_perim = float(contract.get("perimeter_km", perimeter_km))
        if not within_tolerance(area_ha, expected_area, tol_area):
            status = "FAIL"
            issues.append("Perimeter area out of tolerance")
        if not within_tolerance(perimeter_km, expected_perim, tol_perim):
            status = "FAIL"
            issues.append("Perimeter length out of tolerance")
    else:
        status = "FAIL"
        issues.append("Perimeter layer not found")

    manifest = {
        "generated_at": datetime.utcnow().isoformat() + "Z",
        "schema": args.schema,
        "expected_layers": expected_layers,
        "actual_layers": int(layer_count),
        "total_features": int(total_features),
        "bounds": {
            "min_lon": extent[0] if extent else None,
            "min_lat": extent[1] if extent else None,
            "max_lon": extent[2] if extent else None,
            "max_lat": extent[3] if extent else None,
        },
        "perimeter_layer": perimeter_layer,
        "perimeter_area_ha": area_ha,
        "perimeter_km": perimeter_km,
        "duplicates": [
            {"layer_name": row[0], "feature_hash": row[1], "count": int(row[2])}
            for row in duplicates
        ],
        "invalid_geometries": int(invalid),
        "srid_mismatch": int(srid_mismatch),
        "status": status,
        "issues": issues,
    }

    lines: List[str] = []
    lines.append("# validation_report")
    lines.append("")
    lines.append(f"Generated: {manifest['generated_at']}")
    lines.append(f"Schema: {args.schema}")
    lines.append(f"Status: {status}")
    lines.append("")
    lines.append("## Summary")
    lines.append("")
    lines.append(f"- Expected layers: {expected_layers}")
    lines.append(f"- Actual layers: {layer_count}")
    lines.append(f"- Total features: {total_features}")
    if extent:
        lines.append(f"- Extent: {extent}")
    if perimeter_layer:
        lines.append(f"- Perimeter layer: {perimeter_layer}")
        lines.append(f"- Area (ha): {area_ha:.2f}")
        lines.append(f"- Perimeter (km): {perimeter_km:.2f}")
    lines.append(f"- Invalid geometries: {invalid}")
    lines.append(f"- SRID mismatch: {srid_mismatch}")
    lines.append(f"- Duplicate geometries: {len(duplicates)}")

    if issues:
        lines.append("")
        lines.append("## Issues")
        for issue in issues:
            lines.append(f"- {issue}")

    out_report = os.path.abspath(args.out_report)
    os.makedirs(os.path.dirname(out_report), exist_ok=True)
    try:
        with open(out_report, "w", encoding="utf-8", newline="\n") as handle:
            handle.write("\n".join(lines) + "\n")
    except Exception as exc:
        print(f"Failed to write report '{out_report}': {exc}", file=sys.stderr)
        sys.exit(2)

    out_manifest = os.path.abspath(args.out_manifest)
    os.makedirs(os.path.dirname(out_manifest), exist_ok=True)
    try:
        with open(out_manifest, "w", encoding="utf-8", newline="\n") as handle:
            json.dump(manifest, handle, ensure_ascii=False, indent=2)
            handle.write("\n")
    except Exception as exc:
        print(f"Failed to write manifest '{out_manifest}': {exc}", file=sys.stderr)
        sys.exit(2)

    return 0 if status == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
