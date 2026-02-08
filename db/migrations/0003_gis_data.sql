-- GIS data compatibility layer
-- Safe to run multiple times (no destructive operations)

CREATE SCHEMA IF NOT EXISTS gis_data;

CREATE TABLE IF NOT EXISTS gis_data.features (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(255) NOT NULL,
    category VARCHAR(100) NOT NULL,
    subcategory VARCHAR(100),
    layer_name VARCHAR(100) NOT NULL,
    geometry GEOMETRY(GEOMETRY, 4326),
    area_ha NUMERIC(12, 4),
    perimeter_km NUMERIC(12, 4),
    attributes JSONB,
    source_kml VARCHAR(255),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    feature_hash TEXT
);

CREATE INDEX IF NOT EXISTS idx_gis_features_layer
    ON gis_data.features (layer_name);

CREATE INDEX IF NOT EXISTS idx_gis_features_geometry
    ON gis_data.features USING GIST (geometry);

CREATE UNIQUE INDEX IF NOT EXISTS uq_gis_features_source_layer_hash
    ON gis_data.features (source_kml, layer_name, feature_hash);

CREATE OR REPLACE VIEW gis_data.geo_features AS
SELECT
    id,
    name,
    category,
    subcategory,
    layer_name,
    geometry,
    area_ha,
    perimeter_km,
    attributes,
    source_kml,
    created_at,
    updated_at,
    feature_hash
FROM villa_canabrava.geo_features;
