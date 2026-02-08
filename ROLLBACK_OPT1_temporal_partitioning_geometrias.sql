-- ROLLBACK SCRIPT: OPT1 - Temporal Partitioning of Geometrias
-- Purpose: Reverse the temporal partitioning structure created in OPT1
-- Created: 2026-02-06
-- Status: STAGE 3 - Rollback Validation
-- WARNING: This script will DROP partitioned tables and indexes

BEGIN;

-- ============================================================================
-- PARTE 1: Drop Indexes on Partitions
-- ============================================================================

DROP INDEX IF EXISTS idx_catalogo_geometrias_particionada_2026_geom;
DROP INDEX IF EXISTS idx_catalogo_geometrias_particionada_2027_geom;
DROP INDEX IF EXISTS idx_catalogo_geometrias_particionada_2028_geom;

DROP INDEX IF EXISTS idx_catalogo_geometrias_particionada_2026_catalogo_is_valid;
DROP INDEX IF EXISTS idx_catalogo_geometrias_particionada_2027_catalogo_is_valid;
DROP INDEX IF EXISTS idx_catalogo_geometrias_particionada_2028_catalogo_is_valid;

-- ============================================================================
-- PARTE 2: Drop Partition Tables
-- ============================================================================

DROP TABLE IF EXISTS catalogo_geometrias_particionada_2026;
DROP TABLE IF EXISTS catalogo_geometrias_particionada_2027;
DROP TABLE IF EXISTS catalogo_geometrias_particionada_2028;

-- ============================================================================
-- PARTE 3: Drop Partitioned Table
-- ============================================================================

DROP TABLE IF EXISTS catalogo_geometrias_particionada;

-- ============================================================================
-- PARTE 4: Verification & Logging
-- ============================================================================

-- Log rollback execution
INSERT INTO audit_log (action, table_name, description, status, executed_at)
VALUES (
    'ROLLBACK',
    'catalogo_geometrias_particionada',
    'OPT1 Rollback: Removed temporal partitioning structure (2026-2028 partitions)',
    'SUCCESS',
    CURRENT_TIMESTAMP
)
ON CONFLICT DO NOTHING;

COMMIT;

-- ============================================================================
-- ROLLBACK VERIFICATION QUERIES
-- ============================================================================

-- Verify table is dropped
-- SELECT count(*) FROM information_schema.tables 
-- WHERE table_name = 'catalogo_geometrias_particionada';
-- Expected: 0 rows (table does not exist)

-- Verify indexes are dropped
-- SELECT count(*) FROM pg_indexes 
-- WHERE indexname LIKE 'idx_catalogo_geometrias_particionada%';
-- Expected: 0 rows (all indexes dropped)
