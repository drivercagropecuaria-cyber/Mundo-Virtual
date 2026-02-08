import argparse
import glob
import hashlib
import json
import os
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple

import psycopg2
from psycopg2.extras import execute_values

NAME_KEYS = ["name", "Name", "NOME", "nome", "label", "LABEL", "id", "ID", "codigo", "CODIGO"]

def guess_layer_category(stem: str) -> Tuple[str, Optional[str]]:
    # Ex.: "MATA_142" => ("MATA", "142"); "RL_05" => ("RL","05"); "CERCAS" => ("CERCAS", None)
    if "_" in stem:
        a, b = stem.split("_", 1)
        return a.strip(), b.strip() if b.strip() else None
    return stem.strip(), None

def pick_name(props: Dict[str, Any]) -> Optional[str]:
    for k in NAME_KEYS:
        v = props.get(k)
        if v is None:
            continue
        s = str(v).strip()
        if s:
            return s[:500]
    return None

def canonical_hash(geom: Any, props: Any) -> str:
    payload = {
        "geometry": geom,
        "properties": props,
    }
    s = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return hashlib.sha256(s.encode("utf-8")).hexdigest()

def load_geojson(path: Path) -> List[Dict[str, Any]]:
    data = json.loads(path.read_text(encoding="utf-8-sig"))
    if isinstance(data, dict) and data.get("type") == "FeatureCollection":
        feats = data.get("features") or []
        return [f for f in feats if isinstance(f, dict)]
    if isinstance(data, dict) and data.get("type") == "Feature":
        return [data]
    raise ValueError(f"{path}: GeoJSON não é FeatureCollection/Feature")

def detect_srid_from_crs(root: Any, default_srid: int) -> int:
    # GeoJSON moderno normalmente não traz CRS; assumimos 4326.
    try:
        if isinstance(root, dict) and "crs" in root and isinstance(root["crs"], dict):
            crs = root["crs"]
            props = crs.get("properties") or {}
            name = props.get("name")
            if isinstance(name, str) and "EPSG" in name.upper():
                # "EPSG:4326" ou "urn:ogc:def:crs:EPSG::4326"
                digits = "".join(ch for ch in name if ch.isdigit())
                if digits:
                    return int(digits)
    except Exception:
        pass
    return default_srid

def main() -> None:
    ap = argparse.ArgumentParser(description="Import GeoJSON -> PostGIS (villa_canabrava.geo_features)")
    ap.add_argument("--dsn", required=True, help='Ex.: "host=localhost port=5432 dbname=postgres user=postgres" (usa PGPASSWORD se precisar)')
    ap.add_argument("--schema", default="villa_canabrava")
    ap.add_argument("--input", required=True, help='Glob, ex.: ".\\out\\golden\\*.geojson"')
    ap.add_argument("--default-srid", type=int, default=4326)
    ap.add_argument("--batch", type=int, default=1000)
    args = ap.parse_args()

    files = [Path(p) for p in glob.glob(args.input)]
    files = [p for p in files if p.is_file()]
    if not files:
        raise SystemExit(f"Nenhum arquivo encontrado para: {args.input}")

    conn = psycopg2.connect(args.dsn)
    conn.autocommit = False

    insert_sql = f"""
    INSERT INTO {args.schema}.layers (name, category)
    VALUES (%s, %s)
    ON CONFLICT (name) DO NOTHING;
    """

    # geo_features: inserir com ON CONFLICT DO NOTHING (idempotência)
    # Observação: usamos source_kml como "source id" genérico do arquivo (serve p/ unicidade).
    values_sql = f"""
    INSERT INTO {args.schema}.geo_features
      (layer_name, category, subcategory, name, attributes, props, geometry,
       source_file, source_kml, feature_hash, imported_at, fix_flags, area_ha, perimeter_km)
    VALUES %s
    ON CONFLICT (source_kml, layer_name, feature_hash) DO NOTHING;
    """

    # Recalcular métricas pós-insert (uma vez por arquivo)
    metrics_sql = f"""
    UPDATE {args.schema}.geo_features gf
    SET
      area_ha = CASE
        WHEN gf.geometry IS NULL THEN NULL
        WHEN GeometryType(gf.geometry) IN ('POLYGON','MULTIPOLYGON') THEN (ST_Area(gf.geometry::geography) / 10000.0)
        ELSE NULL
      END,
      perimeter_km = CASE
        WHEN gf.geometry IS NULL THEN NULL
        WHEN GeometryType(gf.geometry) IN ('LINESTRING','MULTILINESTRING') THEN (ST_Length(gf.geometry::geography) / 1000.0)
        WHEN GeometryType(gf.geometry) IN ('POLYGON','MULTIPOLYGON') THEN (ST_Perimeter(gf.geometry::geography) / 1000.0)
        ELSE NULL
      END
    WHERE gf.source_kml = %s AND gf.layer_name = %s
      AND (gf.area_ha IS NULL OR gf.perimeter_km IS NULL);
    """

    try:
        with conn.cursor() as cur:
            for path in files:
                stem = path.stem
                category, subcat = guess_layer_category(stem)

                # garantir layer
                cur.execute(insert_sql, (stem, category))

                # carregar json bruto pra detectar srid se houver
                raw = path.read_text(encoding="utf-8-sig")
                root = json.loads(raw)
                srid = detect_srid_from_crs(root, args.default_srid)

                features = load_geojson(path)

                rows = []
                source_file = str(path).replace("\\", "/")
                source_kml = source_file  # nome do campo histórico  usamos como source id

                for f in features:
                    geom = f.get("geometry")
                    if not geom:
                        continue
                    props = f.get("properties") or {}
                    if not isinstance(props, dict):
                        props = {"_raw": props}

                    nm = pick_name(props)
                    # attributes: por enquanto, espelhamos props (depois você pode normalizar)
                    attributes = props

                    fh = canonical_hash(geom, props)

                    rows.append((
                        stem, category, subcat, nm,
                        json.dumps(attributes, ensure_ascii=False),
                        json.dumps(props, ensure_ascii=False),
                        json.dumps(geom, ensure_ascii=False),
                        source_file, source_kml, fh,
                        "{}"
                    ))

                    if len(rows) >= args.batch:
                        _flush(cur, values_sql, rows, srid)
                        rows.clear()

                if rows:
                    _flush(cur, values_sql, rows, srid)

                # métricas por arquivo
                cur.execute(metrics_sql, (source_kml, stem))

                conn.commit()
                print(f"OK: {path}  (features: {len(features)})")

    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()

def _flush(cur, values_sql: str, rows: List[tuple], srid: int) -> None:
    # Ajusta placeholders para geometry e jsonb no VALUES:
    # - attributes/props entram como jsonb via ::jsonb
    # - geometry entra via ST_SetSRID(ST_GeomFromGeoJSON(%s), srid)
    tpl = (
        "(%s,%s,%s,%s,"
        " %s::jsonb, %s::jsonb,"
        f" ST_SetSRID(ST_GeomFromGeoJSON(%s), {srid}),"
        " %s,%s,%s,"
        " now(), COALESCE(%s::jsonb,'{}'::jsonb),"
        " NULL, NULL)"
    )
    execute_values(cur, values_sql, rows, template=tpl, page_size=1000)

if __name__ == "__main__":
    main()
