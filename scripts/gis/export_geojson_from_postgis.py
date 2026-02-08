#!/usr/bin/env python3
"""
Export GeoJSON per layer from PostGIS.
"""

import argparse
import json
import os
from pathlib import Path
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


def sanitize_filename(value: str) -> str:
    cleaned = "".join(ch if ch.isalnum() or ch in ("-", "_") else "_" for ch in value)
    return cleaned.strip("_") or "layer"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Export GeoJSON per layer from PostGIS")
    parser.add_argument("--db-url", default="", help="PostgreSQL connection URL")
    parser.add_argument("--schema", default="villa_canabrava", help="Target schema")
    parser.add_argument("--output-dir", default="exports/geojson", help="Output directory")
    parser.add_argument("--simplify", type=float, default=0.0, help="Simplify tolerance (0 disables)")
    parser.add_argument("--report-out", default="reports/05_export.md", help="Export report output")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    db_url = build_db_url(args)

    out_dir = Path(args.output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    conn = psycopg2.connect(db_url)
    cur = conn.cursor()

    cur.execute(
        f"SELECT DISTINCT layer_name FROM {args.schema}.geo_features ORDER BY layer_name"
    )
    layers = [row[0] for row in cur.fetchall()]

    report_lines: List[str] = []
    report_lines.append("# Relatorio de exportacao GeoJSON")
    report_lines.append("")
    report_lines.append(f"Schema: {args.schema}")
    report_lines.append(f"Output dir: {out_dir.as_posix()}")
    report_lines.append(f"Simplify tolerance: {args.simplify}")
    report_lines.append("")
    report_lines.append("## Layers exportadas")
    report_lines.append("")
    report_lines.append("| layer_name | features | arquivo |")
    report_lines.append("| --- | --- | --- |")

    geom_expr = "geometry"
    if args.simplify and args.simplify > 0:
        geom_expr = f"ST_SimplifyPreserveTopology(geometry, {args.simplify})"

    for layer in layers:
        cur.execute(
            f"""
            SELECT
                name,
                category,
                subcategory,
                layer_name,
                source_kml,
                area_ha,
                perimeter_km,
                attributes,
                ST_AsGeoJSON({geom_expr})
            FROM {args.schema}.geo_features
            WHERE layer_name = %s AND geometry IS NOT NULL
            """,
            (layer,),
        )
        rows = cur.fetchall()

        features = []
        for row in rows:
            (
                name,
                category,
                subcategory,
                layer_name,
                source_kml,
                area_ha,
                perimeter_km,
                attributes,
                geom_json,
            ) = row
            if not geom_json:
                continue
            props: Dict = {}
            props.update(attributes or {})
            props.update(
                {
                    "name": name,
                    "category": category,
                    "subcategory": subcategory,
                    "layer_name": layer_name,
                    "source_kml": source_kml,
                    "area_ha": float(area_ha) if area_ha is not None else None,
                    "perimeter_km": float(perimeter_km) if perimeter_km is not None else None,
                }
            )
            features.append(
                {
                    "type": "Feature",
                    "geometry": json.loads(geom_json),
                    "properties": props,
                }
            )

        collection = {"type": "FeatureCollection", "features": features}
        filename = f"{sanitize_filename(layer)}.geojson"
        out_path = out_dir / filename
        with open(out_path, "w", encoding="utf-8") as handle:
            json.dump(collection, handle, ensure_ascii=False)

        report_lines.append(f"| {layer} | {len(features)} | {out_path.as_posix()} |")

    cur.close()
    conn.close()

    report_path = Path(args.report_out)
    report_path.parent.mkdir(parents=True, exist_ok=True)
    with open(report_path, "w", encoding="utf-8") as handle:
        handle.write("\n".join(report_lines))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
