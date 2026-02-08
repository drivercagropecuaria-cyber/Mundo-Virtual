-- Canonical schema initialization for Mundo Virtual Villa Canabrava
-- Safe to run multiple times (no destructive operations)

CREATE EXTENSION IF NOT EXISTS postgis;
CREATE EXTENSION IF NOT EXISTS postgis_topology;
CREATE EXTENSION IF NOT EXISTS pg_trgm;
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE SCHEMA IF NOT EXISTS villa_canabrava;

CREATE TABLE IF NOT EXISTS villa_canabrava.layers (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(100) NOT NULL UNIQUE,
    display_name VARCHAR(255),
    description TEXT,
    category VARCHAR(100),
    style_config JSONB,
    is_visible BOOLEAN DEFAULT true,
    z_index INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS villa_canabrava.geo_features (
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
    CONSTRAINT fk_layers
        FOREIGN KEY (layer_name)
        REFERENCES villa_canabrava.layers(name)
);

CREATE TABLE IF NOT EXISTS villa_canabrava.museum_items (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    title VARCHAR(255) NOT NULL,
    description TEXT,
    category VARCHAR(100),
    tags TEXT[],
    media_url TEXT,
    location GEOMETRY(POINT, 4326),
    metadata JSONB,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_layers_category
    ON villa_canabrava.layers (category);

CREATE INDEX IF NOT EXISTS idx_geo_features_layer
    ON villa_canabrava.geo_features (layer_name);

CREATE INDEX IF NOT EXISTS idx_geo_features_category
    ON villa_canabrava.geo_features (category);

CREATE INDEX IF NOT EXISTS idx_geo_features_geometry
    ON villa_canabrava.geo_features USING GIST (geometry);

CREATE INDEX IF NOT EXISTS idx_geo_features_name_gin
    ON villa_canabrava.geo_features USING GIN (name gin_trgm_ops);

CREATE INDEX IF NOT EXISTS idx_geo_features_attributes_gin
    ON villa_canabrava.geo_features USING GIN (attributes);

CREATE INDEX IF NOT EXISTS idx_museum_items_location
    ON villa_canabrava.museum_items USING GIST (location);

CREATE INDEX IF NOT EXISTS idx_museum_items_tags
    ON villa_canabrava.museum_items USING GIN (tags);
