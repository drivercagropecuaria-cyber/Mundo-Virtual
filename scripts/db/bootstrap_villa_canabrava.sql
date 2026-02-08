-- scripts/db/bootstrap_villa_canabrava.sql
-- Minimal bootstrap for pipeline/validation
-- Target: villa_canabrava schema + geo_features table (geometry column)

BEGIN;

CREATE EXTENSION IF NOT EXISTS postgis;
CREATE EXTENSION IF NOT EXISTS pgcrypto;
CREATE EXTENSION IF NOT EXISTS pg_trgm;

CREATE SCHEMA IF NOT EXISTS villa_canabrava;

-- Base table expected by tests/queries
CREATE TABLE IF NOT EXISTS villa_canabrava.geo_features (
  id           bigserial PRIMARY KEY,
  layer_name   text NOT NULL,
  feature_hash text,
  geometry     geometry(GEOMETRY, 4326) NOT NULL,
  props        jsonb,
  source_file  text,
  fix_flags    jsonb NOT NULL DEFAULT '{}'::jsonb,
  imported_at  timestamptz NOT NULL DEFAULT now()
);

-- Essential indexes
CREATE INDEX IF NOT EXISTS gx_geo_features_geometry
  ON villa_canabrava.geo_features USING GIST (geometry);

CREATE INDEX IF NOT EXISTS ix_geo_features_layer_name
  ON villa_canabrava.geo_features (layer_name);

-- Idempotency by hash
CREATE UNIQUE INDEX IF NOT EXISTS ux_geo_features_layer_hash
  ON villa_canabrava.geo_features (layer_name, feature_hash)
  WHERE feature_hash IS NOT NULL;

COMMIT;

BEGIN;

ALTER TABLE IF EXISTS villa_canabrava.geo_features
  ADD COLUMN IF NOT EXISTS subcategory text,
  ADD COLUMN IF NOT EXISTS area_ha numeric,
  ADD COLUMN IF NOT EXISTS perimeter_km numeric;

ALTER TABLE IF EXISTS villa_canabrava.layers
  ADD COLUMN IF NOT EXISTS area_ha numeric,
  ADD COLUMN IF NOT EXISTS perimeter_km numeric;

UPDATE villa_canabrava.geo_features
SET subcategory = category
WHERE subcategory IS NULL;

COMMIT;

BEGIN;

-- Corrige drift do schema quando geo_features ja existia (bootstrap/manual)
ALTER TABLE IF EXISTS villa_canabrava.geo_features
  ADD COLUMN IF NOT EXISTS category    text,
  ADD COLUMN IF NOT EXISTS subcategory text,
  ADD COLUMN IF NOT EXISTS name        text,
  ADD COLUMN IF NOT EXISTS attributes  jsonb,
  ADD COLUMN IF NOT EXISTS source_kml  text;

-- Normaliza NULLs para facilitar indices/queries
UPDATE villa_canabrava.geo_features
SET attributes = '{}'::jsonb
WHERE attributes IS NULL;

-- Simple backfill: if subcategory is missing, mirror category
UPDATE villa_canabrava.geo_features
SET subcategory = category
WHERE subcategory IS NULL;

COMMIT;
