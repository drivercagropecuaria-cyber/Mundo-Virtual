-- ROLLBACK SCRIPT: OPT2 - Columnar Storage for GIS Data
-- Purpose: Reverse the columnar storage structures created in OPT2
-- Created: 2026-02-06
-- Status: STAGE 3 - Rollback Validation

BEGIN;

-- ============================================================================
-- PARTE 1: Drop Functions
-- ============================================================================

DROP FUNCTION IF EXISTS refresh_mv_catalogo_geometrias_stats();
DROP FUNCTION IF EXISTS populate_bounds_cache(BIGINT);

-- ============================================================================
-- PARTE 2: Drop Materialized Views
-- ============================================================================

DROP MATERIALIZED VIEW IF EXISTS mv_catalogo_geometrias_stats;

-- ============================================================================
-- PARTE 3: Drop Indexes on Cache Table
-- ============================================================================

DROP INDEX IF EXISTS idx_catalogo_bounds_cache_validated;
DROP INDEX IF EXISTS idx_catalogo_bounds_cache_updated;

-- ============================================================================
-- PARTE 4: Drop Cache Table
-- ============================================================================

DROP TABLE IF EXISTS catalogo_bounds_cache;

-- ============================================================================
-- PARTE 5: Verification & Logging
-- ============================================================================

INSERT INTO audit_log (action, table_name, description, status, executed_at)
VALUES (
    'ROLLBACK',
    'catalogo_bounds_cache, mv_catalogo_geometrias_stats',
    'OPT2 Rollback: Removed columnar storage structures (MV, cache table, functions)',
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
-- WHERE matviewname = 'mv_catalogo_geometrias_stats';
-- Expected: 0 rows

-- Verify cache table is dropped
-- SELECT count(*) FROM information_schema.tables 
-- WHERE table_name = 'catalogo_bounds_cache';
-- Expected: 0 rows

-- Verify functions are dropped
-- SELECT count(*) FROM pg_proc 
-- WHERE proname IN ('refresh_mv_catalogo_geometrias_stats', 'populate_bounds_cache');
-- Expected: 0 rows
