-- Sprint 2 Otimização 1: Particionamento Temporal de Geometrias
-- Purpose: Melhorar performance de queries geoespaciais através de particionamento por data
-- Created: 2026-02-06
-- Migration: 1770470100

BEGIN;

-- Criar tabela particionada por ano para geometrias
-- Strategy: RANGE partitioning por created_at (ano)
CREATE TABLE IF NOT EXISTS catalogo_geometrias_particionada (
    id BIGSERIAL NOT NULL,
    catalogo_id BIGINT NOT NULL,
    geom GEOMETRY(MULTIPOLYGON, 4326) NOT NULL,
    is_valid BOOLEAN DEFAULT FALSE,
    validity_error_msg TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    PRIMARY KEY (id, created_at)
) PARTITION BY RANGE (YEAR(created_at));

-- Comentário descritivo
COMMENT ON TABLE catalogo_geometrias_particionada IS 
'Tabela particionada para otimizar queries de geometrias por período temporal. 
Cada partição agrupa dados de um ano civil completo.';

-- Criar partições para os próximos 3 anos (2026, 2027, 2028)
CREATE TABLE catalogo_geometrias_2026 PARTITION OF catalogo_geometrias_particionada
    FOR VALUES FROM (2026) TO (2027);

CREATE TABLE catalogo_geometrias_2027 PARTITION OF catalogo_geometrias_particionada
    FOR VALUES FROM (2027) TO (2028);

CREATE TABLE catalogo_geometrias_2028 PARTITION OF catalogo_geometrias_particionada
    FOR VALUES FROM (2028) TO (2029);

-- Criar índices em cada partição para aceleração geoespacial
CREATE INDEX idx_catalogo_geometrias_2026_geom ON catalogo_geometrias_2026 USING GIST(geom);
CREATE INDEX idx_catalogo_geometrias_2026_valid ON catalogo_geometrias_2026(is_valid);

CREATE INDEX idx_catalogo_geometrias_2027_geom ON catalogo_geometrias_2027 USING GIST(geom);
CREATE INDEX idx_catalogo_geometrias_2027_valid ON catalogo_geometrias_2027(is_valid);

CREATE INDEX idx_catalogo_geometrias_2028_geom ON catalogo_geometrias_2028 USING GIST(geom);
CREATE INDEX idx_catalogo_geometrias_2028_valid ON catalogo_geometrias_2028(is_valid);

-- Criar índice composto para operações comuns (filtro por catálogo + validação)
CREATE INDEX idx_catalogo_geometrias_2026_catid_valid ON catalogo_geometrias_2026(catalogo_id, is_valid);
CREATE INDEX idx_catalogo_geometrias_2027_catid_valid ON catalogo_geometrias_2027(catalogo_id, is_valid);
CREATE INDEX idx_catalogo_geometrias_2028_catid_valid ON catalogo_geometrias_2028(catalogo_id, is_valid);

-- Registrar estatísticas iniciais
-- ANALYZE catalogo_geometrias_particionada;

COMMIT;
