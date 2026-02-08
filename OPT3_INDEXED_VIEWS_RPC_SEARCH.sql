-- Sprint 3 - OPT3: Indexed Views for RPC Search
-- Migration: 1770500300_indexed_views_rpc_search.sql (ENHANCED)
-- Objetivo: Otimizar queries RPC com indexed views
-- Status: NOVO - Sprint 3 Executor  
-- Data: 2026-02-06 20:02 UTC
-- Expected Improvement: 10-15% para RPC search

BEGIN;

-- ============================================================================
-- PARTE 1: Criar índex para RPC search queries
-- ============================================================================

CREATE INDEX IF NOT EXISTS idx_catalogo_rpc_search_text
ON catalogo (theme_name, description)
USING btree;

CREATE INDEX IF NOT EXISTS idx_catalogo_rpc_search_type
ON catalogo (item_type, is_ativo)
WHERE is_ativo = true;

-- ============================================================================
-- PARTE 2: Criar function para RPC search optimizado
-- ============================================================================

CREATE OR REPLACE FUNCTION get_catalogo_search_optimized(
    p_search_text TEXT,
    p_limit INT DEFAULT 50,
    p_offset INT DEFAULT 0
)
RETURNS TABLE (
    id UUID,
    theme_name TEXT,
    description TEXT,
    item_type TEXT,
    feature_count BIGINT,
    relevance_score NUMERIC
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        c.id,
        c.theme_name,
        c.description,
        c.item_type,
        COUNT(cg.id) as feature_count,
        -- Relevance scoring: exact match > contains match
        CASE 
            WHEN c.theme_name ILIKE p_search_text THEN 1.0::NUMERIC
            WHEN c.theme_name ILIKE p_search_text || '%' THEN 0.8::NUMERIC
            WHEN c.theme_name ILIKE '%' || p_search_text || '%' THEN 0.6::NUMERIC
            WHEN c.description ILIKE '%' || p_search_text || '%' THEN 0.4::NUMERIC
            ELSE 0.2::NUMERIC
        END as relevance_score
    FROM catalogo c
    LEFT JOIN catalogo_geometrias_particionada cg ON c.id = cg.catalogo_id
    WHERE c.theme_name ILIKE '%' || p_search_text || '%'
       OR c.description ILIKE '%' || p_search_text || '%'
    GROUP BY c.id, c.theme_name, c.description, c.item_type
    ORDER BY relevance_score DESC, c.theme_name ASC
    LIMIT p_limit
    OFFSET p_offset;
END;
$$ LANGUAGE plpgsql;

-- ============================================================================
-- PARTE 3: Criar indexed view para busca
-- ============================================================================

CREATE MATERIALIZED VIEW mv_catalogo_search_index AS
SELECT 
    c.id,
    c.theme_name,
    c.description,
    c.item_type,
    c.is_ativo,
    COUNT(cg.id) as feature_count,
    MAX(cg.created_at) as last_updated,
    -- GIN index support for text search
    to_tsvector('portuguese', c.theme_name || ' ' || COALESCE(c.description, '')) as search_vector
FROM catalogo c
LEFT JOIN catalogo_geometrias_particionada cg ON c.id = cg.catalogo_id
GROUP BY c.id, c.theme_name, c.description, c.item_type, c.is_ativo;

CREATE UNIQUE INDEX idx_mv_catalogo_search_index 
ON mv_catalogo_search_index (id);

-- GIN index para full-text search (PostgreSQL 12+)
CREATE INDEX idx_mv_catalogo_search_vector 
ON mv_catalogo_search_index USING GIN (search_vector);

-- ============================================================================
-- PARTE 4: Função para refresh de search index
-- ============================================================================

CREATE OR REPLACE FUNCTION refresh_mv_catalogo_search_index()
RETURNS TABLE(view_name TEXT, status TEXT, duration_ms NUMERIC) AS $$
DECLARE
    v_start_time TIMESTAMP;
    v_duration NUMERIC;
BEGIN
    v_start_time := CURRENT_TIMESTAMP;
    
    REFRESH MATERIALIZED VIEW CONCURRENTLY mv_catalogo_search_index;
    
    v_duration := EXTRACT(EPOCH FROM (CURRENT_TIMESTAMP - v_start_time)) * 1000;
    
    RETURN QUERY SELECT 'mv_catalogo_search_index'::TEXT, 'REFRESHED'::TEXT, v_duration;
END;
$$ LANGUAGE plpgsql;

-- ============================================================================
-- PARTE 5: Função otimizada de RPC search com caching
-- ============================================================================

CREATE OR REPLACE FUNCTION get_catalogo_by_search_rpc(
    p_search_text TEXT,
    p_limit INT DEFAULT 50
)
RETURNS JSON AS $$
DECLARE
    v_result JSON;
BEGIN
    SELECT json_agg(
        jsonb_build_object(
            'id', id::TEXT,
            'theme_name', theme_name,
            'description', description,
            'item_type', item_type,
            'feature_count', feature_count,
            'last_updated', last_updated::TEXT
        )
        ORDER BY feature_count DESC
    ) INTO v_result
    FROM mv_catalogo_search_index
    WHERE search_vector @@ plainto_tsquery('portuguese', p_search_text)
    LIMIT p_limit;
    
    RETURN COALESCE(v_result, '[]'::JSON);
END;
$$ LANGUAGE plpgsql;

-- ============================================================================
-- PARTE 6: Criar índices adicionais para RPC performance
-- ============================================================================

CREATE INDEX IF NOT EXISTS idx_opt3_rpc_query_pattern
ON catalogo (item_type, is_ativo, id)
WHERE is_ativo = true;

CREATE INDEX IF NOT EXISTS idx_opt3_rpc_text_search
ON catalogo USING GIN (
    to_tsvector('portuguese', theme_name || ' ' || COALESCE(description, ''))
);

-- ============================================================================
-- PARTE 7: Procedure para otimização de RPC queries
-- ============================================================================

CREATE OR REPLACE PROCEDURE maintain_search_indexes()
LANGUAGE plpgsql
AS $$
BEGIN
    -- Reindex search indexes
    REINDEX INDEX CONCURRENTLY idx_opt3_rpc_text_search;
    REINDEX INDEX CONCURRENTLY idx_catalogo_rpc_search_text;
    
    -- ANALYZE para estatísticas
    ANALYZE catalogo;
    
    -- Refresh search materialized view
    REFRESH MATERIALIZED VIEW CONCURRENTLY mv_catalogo_search_index;
    
    -- Log
    INSERT INTO partition_maintenance_log (action, status, details)
    VALUES ('maintain_search_indexes', 'SUCCESS', 
            jsonb_build_object('indexes_reindexed', 2, 'timestamp', now()));
    
    RAISE NOTICE 'Search index maintenance completed at %', CURRENT_TIMESTAMP;
END;
$$;

-- ============================================================================
-- PARTE 8: Comentários
-- ============================================================================

COMMENT ON FUNCTION get_catalogo_search_optimized(TEXT, INT, INT) IS 
'Optimized RPC search function com relevance scoring.
Expected improvement: 10-15% versus standard FTS (Q4).';

COMMENT ON MATERIALIZED VIEW mv_catalogo_search_index IS 
'Indexed view para busca otimizada com GIN index.
Refresh via refresh_mv_catalogo_search_index().';

COMMENT ON FUNCTION get_catalogo_by_search_rpc(TEXT, INT) IS 
'RPC-compatible search function retornando JSON.
Utiliza GIN index para full-text search performance.';

-- ============================================================================
-- PARTE 9: Verificação
-- ============================================================================

SELECT 
    indexname,
    pg_size_pretty(pg_relation_size(indexrelid)) AS size
FROM pg_indexes
WHERE tablename IN ('catalogo', 'mv_catalogo_search_index')
AND indexname LIKE 'idx_opt3%' OR indexname LIKE 'idx_catalogo_rpc%'
ORDER BY indexname;

COMMIT;

-- ============================================================================
-- NOTAS:
-- ============================================================================
-- 1. OPT3 fokus pada RPC search (Q4)
-- 2. GIN index untuk full-text search
-- 3. Materialized view pre-calculates search vector
-- 4. Relevance scoring untuk better UX
-- 5. JSON RPC output format ready
--
-- TESTING:
-- SELECT * FROM get_catalogo_search_optimized('theme_name', 10, 0);
-- SELECT get_catalogo_by_search_rpc('search_term', 50);
-- SELECT refresh_mv_catalogo_search_index();
-- CALL maintain_search_indexes();
--
-- EXPECTED RESULTS:
-- - Q4 latency: 145.8 ms → 123-131 ms (-10-15%)
-- - RPC search: 2x faster with relevance ranking
--
