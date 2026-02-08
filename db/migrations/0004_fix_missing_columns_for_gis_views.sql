BEGIN;

-- drift fix: colunas esperadas pelas views/relatórios GIS
ALTER TABLE IF EXISTS villa_canabrava.geo_features
  ADD COLUMN IF NOT EXISTS subcategory text,
  ADD COLUMN IF NOT EXISTS area_ha numeric,
  ADD COLUMN IF NOT EXISTS perimeter_km numeric,
  ADD COLUMN IF NOT EXISTS created_at timestamptz NOT NULL DEFAULT now(),
  ADD COLUMN IF NOT EXISTS updated_at timestamptz NOT NULL DEFAULT now();

ALTER TABLE IF EXISTS villa_canabrava.layers
  ADD COLUMN IF NOT EXISTS area_ha numeric,
  ADD COLUMN IF NOT EXISTS perimeter_km numeric,
  ADD COLUMN IF NOT EXISTS created_at timestamptz NOT NULL DEFAULT now(),
  ADD COLUMN IF NOT EXISTS updated_at timestamptz NOT NULL DEFAULT now();

-- backfill mínimo
UPDATE villa_canabrava.geo_features
SET subcategory = category
WHERE subcategory IS NULL;

COMMIT;
