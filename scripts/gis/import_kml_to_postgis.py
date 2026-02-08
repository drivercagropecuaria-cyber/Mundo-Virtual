#!/usr/bin/env python3
"""
Import KML/KMZ files into the canonical villa_canabrava schema.
"""

import argparse
import csv
import hashlib
import json
import logging
import os
import sys
import unicodedata
import zipfile
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Tuple

import fiona
import psycopg2
from psycopg2 import extras
from pyproj import Geod
from shapely.geometry import GeometryCollection, LineString, Point, Polygon, shape
from shapely.geometry.base import BaseGeometry
import xml.etree.ElementTree as ET

fiona.drvsupport.supported_drivers["KML"] = "rw"
fiona.drvsupport.supported_drivers["LIBKML"] = "rw"

LAYER_MAPPING = {
    "PIVO": {"category": "Infraestrutura", "subcategory": "Irrigacao"},
    "POCO": {"category": "Infraestrutura", "subcategory": "Abastecimento"},
    "CERCA": {"category": "Limite", "subcategory": "Divisao"},
    "MATA": {"category": "Ambiental", "subcategory": "Mata Nativa"},
    "APP": {"category": "Ambiental", "subcategory": "Preservacao"},
    "RESERVA_LEGAL": {"category": "Ambiental", "subcategory": "Reserva Legal"},
    "CASA_COLONO": {"category": "Edificacao", "subcategory": "Residencial"},
    "SEDE": {"category": "Edificacao", "subcategory": "Administrativo"},
    "PISTA_VAQUEIJADA": {"category": "Lazer", "subcategory": "Eventos"},
    "CONFINAMENTO": {"category": "Infraestrutura", "subcategory": "Produtiva"},
    "CURRAL": {"category": "Infraestrutura", "subcategory": "Produtiva"},
    "SILO": {"category": "Infraestrutura", "subcategory": "Armazenamento"},
    "FABRICA_RACAO": {"category": "Infraestrutura", "subcategory": "Produtiva"},
    "BREJO": {"category": "Ambiental", "subcategory": "Hidrico"},
    "LAGOA": {"category": "Ambiental", "subcategory": "Hidrico"},
    "CORREGO": {"category": "Ambiental", "subcategory": "Hidrico"},
    "ESTRADA": {"category": "Transporte", "subcategory": "Rodoviario"},
    "FERROVIA": {"category": "Transporte", "subcategory": "Ferroviario"},
    "AERODROMO": {"category": "Transporte", "subcategory": "Aereo"},
    "TALHAO": {"category": "Produtiva", "subcategory": "Manejo"},
}

GEOD = Geod(ellps="WGS84")


def normalize_text(value: str) -> str:
    value = value.strip().upper()
    return "".join(
        ch for ch in unicodedata.normalize("NFKD", value)
        if not unicodedata.combining(ch)
    )


def detect_category(name: str, layer_name: str, file_name: str) -> Tuple[str, str]:
    haystack = normalize_text(" ".join([name, layer_name, file_name]))
    for key, meta in LAYER_MAPPING.items():
        if key in haystack:
            return meta["category"], meta["subcategory"]
    return "Indefinido", "Indefinido"


def to_jsonable(value):
    if value is None or isinstance(value, (str, int, float, bool)):
        return value
    if isinstance(value, dict):
        return {str(k): to_jsonable(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [to_jsonable(v) for v in value]
    return str(value)


def geom_area_perimeter(geom: BaseGeometry) -> Tuple[float, float]:
    if geom is None or geom.is_empty:
        return 0.0, 0.0
    if geom.geom_type in ("Polygon", "MultiPolygon"):
        area, perimeter = GEOD.geometry_area_perimeter(geom)
        return abs(area) / 10000.0, abs(perimeter) / 1000.0
    if geom.geom_type in ("LineString", "MultiLineString"):
        return 0.0, abs(GEOD.geometry_length(geom)) / 1000.0
    return 0.0, 0.0


def parse_coords(text: str) -> List[Tuple[float, float]]:
    coords = []
    for part in text.strip().split():
        pieces = part.split(",")
        if len(pieces) < 2:
            continue
        coords.append((float(pieces[0]), float(pieces[1])))
    return coords


def read_kml_etree(path: Path) -> Iterable[Dict]:
    if path.suffix.lower() == ".kmz":
        with zipfile.ZipFile(path, "r") as zf:
            kml_names = [n for n in zf.namelist() if n.lower().endswith(".kml")]
            if not kml_names:
                return []
            preferred = None
            for name in kml_names:
                if name.lower().endswith("doc.kml"):
                    preferred = name
                    break
            data = zf.read(preferred or kml_names[0])
    else:
        data = path.read_bytes()

    root = ET.fromstring(data)
    ns_uri = root.tag.split("}")[0].strip("{") if "}" in root.tag else ""
    ns = {"k": ns_uri} if ns_uri else {}

    def find_text(node, tag, default=""):
        if ns:
            return node.findtext(tag, default=default, namespaces=ns)
        return node.findtext(tag, default=default)

    def extract_geom(placemark):
        point_nodes = placemark.findall(".//k:Point", ns) if ns else placemark.findall(".//Point")
        for pt in point_nodes:
            coord_text = find_text(pt, "k:coordinates" if ns else "coordinates")
            if coord_text:
                coords = parse_coords(coord_text)
                if coords:
                    return Point(coords[0])

        line_nodes = placemark.findall(".//k:LineString", ns) if ns else placemark.findall(".//LineString")
        for line in line_nodes:
            coord_text = find_text(line, "k:coordinates" if ns else "coordinates")
            if coord_text:
                coords = parse_coords(coord_text)
                if len(coords) >= 2:
                    return LineString(coords)

        poly_nodes = placemark.findall(".//k:Polygon", ns) if ns else placemark.findall(".//Polygon")
        for poly in poly_nodes:
            outer_text = find_text(
                poly,
                ".//k:outerBoundaryIs/k:LinearRing/k:coordinates" if ns else ".//outerBoundaryIs/LinearRing/coordinates",
            )
            if outer_text:
                outer = parse_coords(outer_text)
                if len(outer) >= 3:
                    return Polygon(outer)

        return None

    placemarks = root.findall(".//k:Placemark", ns) if ns else root.findall(".//Placemark")
    features = []
    for pm in placemarks:
        geom = extract_geom(pm)
        if geom is None:
            continue
        features.append(
            {
                "name": find_text(pm, "k:name" if ns else "name", default="") or "Unnamed",
                "description": find_text(pm, "k:description" if ns else "description", default="") or "",
                "geometry": geom,
                "properties": {},
            }
        )
    return features


def read_kml_fiona(path: Path) -> Iterable[Dict]:
    features = []
    try:
        layers = fiona.listlayers(str(path))
    except Exception:
        layers = [None]

    for layer in layers:
        try:
            with fiona.open(str(path), layer=layer, driver="KML") as src:
                for feat in src:
                    geom = shape(feat.get("geometry")) if feat.get("geometry") else None
                    props = feat.get("properties") or {}
                    features.append(
                        {
                            "name": props.get("Name") or props.get("name") or "Unnamed",
                            "description": props.get("Description") or props.get("description") or "",
                            "geometry": geom,
                            "properties": props,
                        }
                    )
        except Exception:
            continue
    return features


def iter_features(path: Path) -> Iterable[Dict]:
    try:
        features = read_kml_fiona(path)
    except Exception:
        return read_kml_etree(path)
    if features:
        return features
    return read_kml_etree(path)


def connect(db_url: str):
    return psycopg2.connect(db_url)


def ensure_layer(conn, schema: str, layer_name: str, display_name: str, category: str):
    with conn.cursor() as cur:
        cur.execute(
            f"""
            INSERT INTO {schema}.layers (name, display_name, category)
            VALUES (%s, %s, %s)
            ON CONFLICT (name)
            DO UPDATE SET display_name = EXCLUDED.display_name,
                          category = EXCLUDED.category
            """,
            (layer_name, display_name, category),
        )


def insert_features(conn, schema: str, rows: List[Tuple]):
    if not rows:
        return
    with conn.cursor() as cur:
        extras.execute_values(
            cur,
            f"""
            INSERT INTO {schema}.geo_features
                (name, category, subcategory, layer_name, geometry, area_ha, perimeter_km, attributes, source_kml, feature_hash)
            VALUES %s
            ON CONFLICT (source_kml, layer_name, feature_hash)
            DO UPDATE SET
                name = EXCLUDED.name,
                category = EXCLUDED.category,
                subcategory = EXCLUDED.subcategory,
                geometry = EXCLUDED.geometry,
                area_ha = EXCLUDED.area_ha,
                perimeter_km = EXCLUDED.perimeter_km,
                attributes = EXCLUDED.attributes,
                updated_at = NOW()
            """,
            rows,
            template="(%s,%s,%s,%s,ST_Force2D(ST_SetSRID(ST_GeomFromText(%s),4326)),%s,%s,%s,%s,%s)",
            page_size=200,
        )


def delete_by_source(conn, schema: str, source_kml: str):
    with conn.cursor() as cur:
        cur.execute(
            f"DELETE FROM {schema}.geo_features WHERE source_kml = %s",
            (source_kml,),
        )


def hash_feature(name: str, layer_name: str, geom_wkt: str, attributes: Dict) -> str:
    payload = {
        "name": name,
        "layer": layer_name,
        "geometry": geom_wkt,
        "attributes": attributes,
    }
    encoded = json.dumps(payload, sort_keys=True, ensure_ascii=True).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def build_db_url(args: argparse.Namespace) -> str:
    if args.db_url:
        return args.db_url
    host = os.environ.get("DB_HOST", "localhost")
    port = os.environ.get("DB_PORT", "5432")
    db = os.environ.get("DB_NAME", "villa_canabrava")
    user = os.environ.get("DB_USER", "postgres")
    password = os.environ.get("DB_PASSWORD", "postgres")
    return f"postgresql://{user}:{password}@{host}:{port}/{db}"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Import KML/KMZ into PostGIS")
    parser.add_argument("--kml-dir", required=True, help="Directory containing KML/KMZ files")
    parser.add_argument("--db-url", default="", help="PostgreSQL connection URL")
    parser.add_argument("--schema", default="villa_canabrava", help="Target schema")
    parser.add_argument("--summary-out", default="", help="Write JSON summary to file")
    parser.add_argument("--dry-run", action="store_true", help="Parse but do not insert")
    parser.add_argument("--report-dir", default="reports", help="Directory for import reports")
    parser.add_argument(
        "--replace-existing",
        dest="replace_existing",
        action="store_true",
        default=True,
        help="Remove existing rows for each source file before insert",
    )
    parser.add_argument(
        "--no-replace",
        dest="replace_existing",
        action="store_false",
        help="Do not remove existing rows for each source file",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
    logger = logging.getLogger("import_kml")

    kml_dir = Path(args.kml_dir)
    if not kml_dir.exists():
        logger.error("KML directory not found: %s", kml_dir)
        return 1

    db_url = build_db_url(args)
    logger.info("Using schema: %s", args.schema)

    files = [p for p in kml_dir.rglob("*") if p.suffix.lower() in (".kml", ".kmz")]
    if not files:
        logger.error("No KML/KMZ files found in %s", kml_dir)
        return 1

    summary = {"files": 0, "features": 0, "skipped": 0, "errors": 0}
    report_dir = Path(args.report_dir)
    report_dir.mkdir(parents=True, exist_ok=True)
    skipped_rows: List[Dict[str, str]] = []
    import_rows: List[Dict[str, str]] = []

    conn = connect(db_url)
    conn.autocommit = False

    try:
        for path in files:
            summary["files"] += 1
            layer_name = normalize_text(path.stem).replace(" ", "_")
            file_rows = []
            file_skipped = 0
            file_errors = 0
            try:
                features = iter_features(path)
            except Exception:
                summary["errors"] += 1
                file_errors += 1
                skipped_rows.append(
                    {
                        "source_kml": path.name,
                        "layer_name": layer_name,
                        "name": "",
                        "reason": "READ_ERROR_LAYER",
                        "details": "Falha ao ler o arquivo",
                    }
                )
                import_rows.append(
                    {
                        "source_kml": path.name,
                        "features": "0",
                        "skipped": str(file_skipped),
                        "errors": str(file_errors),
                    }
                )
                continue

            for feat in features:
                geom = feat.get("geometry")
                if geom is None or geom.is_empty:
                    summary["skipped"] += 1
                    file_skipped += 1
                    skipped_rows.append(
                        {
                            "source_kml": path.name,
                            "layer_name": layer_name,
                            "name": feat.get("name") or path.stem,
                            "reason": "EMPTY_GEOMETRY",
                            "details": "Geometria vazia ou nula",
                        }
                    )
                    continue
                if not geom.is_valid:
                    summary["skipped"] += 1
                    file_skipped += 1
                    skipped_rows.append(
                        {
                            "source_kml": path.name,
                            "layer_name": layer_name,
                            "name": feat.get("name") or path.stem,
                            "reason": "INVALID_GEOMETRY",
                            "details": "Geometria invalida",
                        }
                    )
                    continue
                if geom.geom_type == "GeometryCollection":
                    summary["skipped"] += 1
                    file_skipped += 1
                    skipped_rows.append(
                        {
                            "source_kml": path.name,
                            "layer_name": layer_name,
                            "name": feat.get("name") or path.stem,
                            "reason": "UNSUPPORTED_GEOMETRY",
                            "details": "GeometryCollection nao suportada",
                        }
                    )
                    continue

                name = feat.get("name") or path.stem
                category, subcategory = detect_category(name, layer_name, path.name)
                area_ha, perimeter_km = geom_area_perimeter(geom)
                raw_props = feat.get("properties") or {}
                attributes = to_jsonable(dict(raw_props))
                attributes["description"] = feat.get("description", "")
                feature_hash = hash_feature(name, layer_name, geom.wkt, attributes)

                ensure_layer(conn, args.schema, layer_name, path.stem, category)

                file_rows.append(
                    (
                        name,
                        category,
                        subcategory,
                        layer_name,
                        geom.wkt,
                        round(area_ha, 4),
                        round(perimeter_km, 4),
                        extras.Json(attributes),
                        path.name,
                        feature_hash,
                    )
                )

            summary["features"] += len(file_rows)
            if args.dry_run:
                logger.info("[DRY-RUN] %s -> %s features", path.name, len(file_rows))
            else:
                if args.replace_existing:
                    delete_by_source(conn, args.schema, path.name)
                insert_features(conn, args.schema, file_rows)
                conn.commit()
                logger.info("Imported %s -> %s features", path.name, len(file_rows))

            import_rows.append(
                {
                    "source_kml": path.name,
                    "features": str(len(file_rows)),
                    "skipped": str(file_skipped),
                    "errors": str(file_errors),
                }
            )

    except Exception as exc:
        conn.rollback()
        logger.exception("Import failed: %s", exc)
        summary["errors"] += 1
        return 1
    finally:
        conn.close()

    logger.info("Done. Files=%s Features=%s Skipped=%s Errors=%s", summary["files"], summary["features"], summary["skipped"], summary["errors"])

    skipped_path = report_dir / "skipped_report.csv"
    import_path = report_dir / "import_report.csv"
    with open(skipped_path, "w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=["source_kml", "layer_name", "name", "reason", "details"],
        )
        writer.writeheader()
        writer.writerows(skipped_rows)

    with open(import_path, "w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=["source_kml", "features", "skipped", "errors"],
        )
        writer.writeheader()
        writer.writerows(import_rows)

    if args.summary_out:
        with open(args.summary_out, "w", encoding="utf-8") as handle:
            json.dump(summary, handle, indent=2)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
