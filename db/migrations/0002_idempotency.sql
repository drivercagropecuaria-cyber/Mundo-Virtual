-- Idempotent import support

ALTER TABLE IF EXISTS villa_canabrava.geo_features
    ADD COLUMN IF NOT EXISTS feature_hash TEXT;

CREATE UNIQUE INDEX IF NOT EXISTS uq_geo_features_source_layer_hash
    ON villa_canabrava.geo_features (source_kml, layer_name, feature_hash);
