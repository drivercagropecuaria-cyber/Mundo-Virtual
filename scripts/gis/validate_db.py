#!/usr/bin/env python3
"""
Validate canonical database schema and generate validation_report.md.
"""

import argparse
import os
from datetime import datetime
from typing import Dict, List, Tuple

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


def parse_bbox(value: str) -> Tuple[float, float, float, float]:
    parts = [float(p.strip()) for p in value.split(",")]
    if len(parts) != 4:
        raise ValueError("expected bbox as min_lon,min_lat,max_lon,max_lat")
    return parts[0], parts[1], parts[2], parts[3]


def query_one(cur, sql: str, params=None):
    cur.execute(sql, params or ())
    return cur.fetchone()[0]


def explain_query(cur, sql: str, params=None) -> str:
    cur.execute(f"EXPLAIN (FORMAT TEXT) {sql}", params or ())
    rows = cur.fetchall()
    return "\n".join(r[0] for r in rows)


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate PostGIS data")
    parser.add_argument("--db-url", default="", help="PostgreSQL connection URL")
    parser.add_argument("--schema", default="villa_canabrava", help="Target schema")
    parser.add_argument("--expected-bbox", default="", help="min_lon,min_lat,max_lon,max_lat")
    parser.add_argument("--output", default="validation_report.md", help="Output report file")
    parser.add_argument(
        "--quality-out",
        default="reports/03_spatial_quality.md",
        help="Output spatial quality report",
    )
    args = parser.parse_args()

    db_url = build_db_url(args)
    expected_bbox = parse_bbox(args.expected_bbox) if args.expected_bbox else None

    conn = psycopg2.connect(db_url)
    cur = conn.cursor()

    postgis_ok = query_one(cur, "SELECT EXISTS (SELECT 1 FROM pg_extension WHERE extname = 'postgis')")
    total = query_one(cur, f"SELECT COUNT(*) FROM {args.schema}.geo_features")
    invalid = query_one(cur, f"SELECT COUNT(*) FROM {args.schema}.geo_features WHERE geometry IS NOT NULL AND NOT ST_IsValid(geometry)")
    srid_mismatch = query_one(cur, f"SELECT COUNT(*) FROM {args.schema}.geo_features WHERE geometry IS NOT NULL AND ST_SRID(geometry) <> 4326")
    null_geom = query_one(cur, f"SELECT COUNT(*) FROM {args.schema}.geo_features WHERE geometry IS NULL")

    cur.execute(
        f"SELECT GeometryType(geometry) AS geom_type, COUNT(*) FROM {args.schema}.geo_features WHERE geometry IS NOT NULL GROUP BY geom_type ORDER BY COUNT(*) DESC"
    )
    geom_counts = cur.fetchall()

    cur.execute(f"SELECT layer_name, COUNT(*) FROM {args.schema}.geo_features GROUP BY layer_name ORDER BY COUNT(*) DESC")
    layer_counts = cur.fetchall()

    cur.execute(f"SELECT ST_Extent(geometry) FROM {args.schema}.geo_features WHERE geometry IS NOT NULL")
    extent = cur.fetchone()[0]

    cur.execute(
        f"""
        SELECT
            ST_XMin(extent_geom),
            ST_YMin(extent_geom),
            ST_XMax(extent_geom),
            ST_YMax(extent_geom)
        FROM (
            SELECT ST_Extent(geometry)::geometry AS extent_geom
            FROM {args.schema}.geo_features
            WHERE geometry IS NOT NULL
        ) s
        """
    )
    extent_bounds = cur.fetchone()
    explain_bbox = ""
    explain_intersects = ""
    if extent_bounds and all(v is not None for v in extent_bounds):
        min_lon, min_lat, max_lon, max_lat = extent_bounds
        bbox_sql = (
            f"SELECT id FROM {args.schema}.geo_features "
            "WHERE geometry && ST_MakeEnvelope(%s, %s, %s, %s, 4326) LIMIT 5"
        )
        intersects_sql = (
            f"SELECT id FROM {args.schema}.geo_features "
            "WHERE ST_Intersects(geometry, ST_MakeEnvelope(%s, %s, %s, %s, 4326)) LIMIT 5"
        )
        explain_bbox = explain_query(cur, bbox_sql, (min_lon, min_lat, max_lon, max_lat))
        explain_intersects = explain_query(cur, intersects_sql, (min_lon, min_lat, max_lon, max_lat))

    extent_ok = True
    extent_note = ""
    if expected_bbox and extent:
        cur.execute(
            f"SELECT ST_Extent(geometry) FROM {args.schema}.geo_features WHERE geometry IS NOT NULL"
        )
        extent_text = cur.fetchone()[0]
        extent_note = f"Extent: {extent_text}"
        min_lon, min_lat, max_lon, max_lat = expected_bbox
        cur.execute(
            f"""
            SELECT
                ST_XMin(extent_geom) >= %s AS min_lon_ok,
                ST_YMin(extent_geom) >= %s AS min_lat_ok,
                ST_XMax(extent_geom) <= %s AS max_lon_ok,
                ST_YMax(extent_geom) <= %s AS max_lat_ok
            FROM (
                SELECT ST_Extent(geometry)::geometry AS extent_geom
                FROM {args.schema}.geo_features
                WHERE geometry IS NOT NULL
            ) s
            """,
            (min_lon, min_lat, max_lon, max_lat),
        )
        flags = cur.fetchone()
        extent_ok = all(flags)

    cur.close()
    conn.close()

    status = "PASS"
    issues: List[str] = []
    if not postgis_ok:
        status = "FAIL"
        issues.append("PostGIS extension not installed")
    if invalid > 0 or srid_mismatch > 0:
        status = "FAIL"
    if null_geom > 0:
        issues.append(f"Null geometries: {null_geom}")
    if invalid > 0:
        issues.append(f"Invalid geometries: {invalid}")
    if srid_mismatch > 0:
        issues.append(f"SRID mismatch: {srid_mismatch}")
    if expected_bbox and not extent_ok:
        status = "WARN" if status == "PASS" else status
        issues.append("Extent outside expected bbox")

    lines: List[str] = []
    lines.append("# validation_report")
    lines.append("")
    lines.append(f"Generated: {datetime.utcnow().isoformat()}Z")
    lines.append(f"Schema: {args.schema}")
    lines.append(f"Status: {status}")
    lines.append("")
    lines.append("## Summary")
    lines.append("")
    lines.append(f"- PostGIS enabled: {'YES' if postgis_ok else 'NO'}")
    lines.append(f"- Total features: {total}")
    lines.append(f"- Null geometry: {null_geom}")
    lines.append(f"- Invalid geometry: {invalid}")
    lines.append(f"- SRID mismatch: {srid_mismatch}")
    if extent:
        lines.append(f"- Extent: {extent}")
    if expected_bbox:
        lines.append(f"- Expected bbox: {expected_bbox}")
        if extent_note:
            lines.append(f"- {extent_note}")
    if issues:
        lines.append("")
        lines.append("## Issues")
        lines.extend([f"- {issue}" for issue in issues])

    lines.append("")
    lines.append("## Counts by layer")
    lines.append("")
    lines.append("| layer_name | count |")
    lines.append("| --- | --- |")
    for layer, count in layer_counts:
        lines.append(f"| {layer} | {count} |")

    quality_lines: List[str] = []
    quality_lines.append("# Relatorio de qualidade espacial")
    quality_lines.append("")
    quality_lines.append(f"Generated: {datetime.utcnow().isoformat()}Z")
    quality_lines.append(f"Schema: {args.schema}")
    quality_lines.append("")
    quality_lines.append("## Saude geral")
    quality_lines.append("")
    quality_lines.append(f"- PostGIS enabled: {'YES' if postgis_ok else 'NO'}")
    quality_lines.append(f"- Total features: {total}")
    quality_lines.append(f"- Null geometry: {null_geom}")
    quality_lines.append(f"- Invalid geometry: {invalid}")
    quality_lines.append(f"- SRID mismatch: {srid_mismatch}")
    if extent:
        quality_lines.append(f"- Extent: {extent}")

    quality_lines.append("")
    quality_lines.append("## Contagem por tipo de geometria")
    quality_lines.append("")
    quality_lines.append("| geom_type | count |")
    quality_lines.append("| --- | --- |")
    for geom_type, count in geom_counts:
        quality_lines.append(f"| {geom_type} | {count} |")

    if explain_bbox:
        quality_lines.append("")
        quality_lines.append("## EXPLAIN - Filtro por bbox")
        quality_lines.append("")
        quality_lines.append("```text")
        quality_lines.append(explain_bbox)
        quality_lines.append("```")

    if explain_intersects:
        quality_lines.append("")
        quality_lines.append("## EXPLAIN - ST_Intersects")
        quality_lines.append("")
        quality_lines.append("```text")
        quality_lines.append(explain_intersects)
        quality_lines.append("```")

    with open(args.output, "w", encoding="utf-8") as handle:
        handle.write("\n".join(lines))

    quality_path = args.quality_out
    quality_dir = os.path.dirname(quality_path)
    if quality_dir:
        os.makedirs(quality_dir, exist_ok=True)
    with open(quality_path, "w", encoding="utf-8") as handle:
        handle.write("\n".join(quality_lines))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
