-- ROLLBACK SCRIPT: OPT3 - Indexed Views + RPC Search
-- Purpose: Reverse the indexed views and RPC functions created in OPT3
-- Created: 2026-02-06
-- Status: STAGE 3 - Rollback Validation

BEGIN;

-- ============================================================================
-- PARTE 1: Drop RPC Functions
-- ============================================================================

DROP FUNCTION IF EXISTS search_catalogo_indexed(
    TEXT, TEXT, BOOLEAN, INT, INT
);

-- ============================================================================
-- PARTE 2: Drop Indexes on Materialized View
-- ============================================================================

DROP INDEX IF EXISTS idx_mv_catalogo_search_vector_pt;
DROP INDEX IF EXISTS idx_mv_catalogo_search_nome;
DROP INDEX IF EXISTS idx_mv_catalogo_search_tipo_status;
DROP INDEX IF EXISTS idx_mv_catalogo_search_is_active_geom;

-- ============================================================================
-- PARTE 3: Drop Materialized View
-- ============================================================================

DROP MATERIALIZED VIEW IF EXISTS mv_catalogo_search_indexed;

-- ============================================================================
-- PARTE 4: Verification & Logging
-- ============================================================================

INSERT INTO audit_log (action, table_name, description, status, executed_at)
VALUES (
    'ROLLBACK',
    'mv_catalogo_search_indexed',
    'OPT3 Rollback: Removed indexed views and RPC search function',
    'SUCCESS',
    CURRENT_TIMESTAMP
)
ON CONFLICT DO NOTHING;

COMMIT;

-- ============================================================================
-- ROLLBACK VERIFICATION QUERIES
-- ============================================================================

-- Verify MV is dropped
-- SELECT count(*) FROM pg_matviews 
-- WHERE matviewname = 'mv_catalogo_search_indexed';
-- Expected: 0 rows

-- Verify RPC function is dropped
-- SELECT count(*) FROM pg_proc 
-- WHERE proname = 'search_catalogo_indexed';
-- Expected: 0 rows

-- Verify indexes are dropped
-- SELECT count(*) FROM pg_indexes 
-- WHERE indexname LIKE 'idx_mv_catalogo_search%';
-- Expected: 0 rows
