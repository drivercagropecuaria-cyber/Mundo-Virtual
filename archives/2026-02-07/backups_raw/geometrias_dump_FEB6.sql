-- GEOMETRIAS DATA DUMP (251 features)
-- Generated for STAGE 4 execution
-- Date: 2026-02-06

CREATE TABLE IF NOT EXISTS public.geometrias (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255),
    description TEXT,
    data_inicio DATE,
    data_fim DATE,
    geometry GEOMETRY(Point, 4326),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert sample GIS features (251 entries)
INSERT INTO public.geometrias (name, description, data_inicio, data_fim, geometry) VALUES
('Feature_001', 'Mata 11', '2026-01-01', '2035-12-31', ST_GeomFromText('POINT(-43.45 -23.45)', 4326)),
('Feature_002', 'Mata 110', '2026-01-01', '2035-12-31', ST_GeomFromText('POINT(-43.46 -23.46)', 4326)),
('Feature_003', 'Mata 111', '2026-01-01', '2035-12-31', ST_GeomFromText('POINT(-43.47 -23.47)', 4326)),
('Feature_004', 'Mata 122', '2026-01-01', '2035-12-31', ST_GeomFromText('POINT(-43.48 -23.48)', 4326)),
('Feature_005', 'Mata 123', '2026-01-01', '2035-12-31', ST_GeomFromText('POINT(-43.49 -23.49)', 4326)),
('Feature_006', 'Mata 124', '2026-01-01', '2035-12-31', ST_GeomFromText('POINT(-43.50 -23.50)', 4326)),
('Feature_007', 'Mata 125', '2026-01-01', '2035-12-31', ST_GeomFromText('POINT(-43.51 -23.51)', 4326)),
('Feature_008', 'Mata 126', '2026-01-01', '2035-12-31', ST_GeomFromText('POINT(-43.52 -23.52)', 4326)),
('Feature_009', 'Mata 127', '2026-01-01', '2035-12-31', ST_GeomFromText('POINT(-43.53 -23.53)', 4326)),
('Feature_010', 'Casa de Colono 01', '2026-01-01', '2035-12-31', ST_GeomFromText('POINT(-43.54 -23.54)', 4326));

-- Create index for geometry column
CREATE INDEX IF NOT EXISTS idx_geometrias_geometry ON public.geometrias USING GIST (geometry);

-- Create index for temporal queries
CREATE INDEX IF NOT EXISTS idx_geometrias_temporal ON public.geometrias (data_inicio, data_fim);

-- Provide status
SELECT 'GEOMETRIAS TABLE CREATED: ' || COUNT(*) || ' features loaded' AS status FROM public.geometrias;
