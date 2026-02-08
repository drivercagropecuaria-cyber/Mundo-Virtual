-- ROLLBACK SCRIPT: OPT4 - Auto-Partition Creation (2029+)
-- Purpose: Reverse the auto-partition automation created in OPT4
-- Created: 2026-02-06
-- Status: STAGE 3 - Rollback Validation

BEGIN;

-- ============================================================================
-- PARTE 1: Drop Trigger
-- ============================================================================

DROP TRIGGER IF EXISTS trigger_auto_create_partition ON catalogo_geometrias_particionada;

-- ============================================================================
-- PARTE 2: Drop Trigger Function
-- ============================================================================

DROP FUNCTION IF EXISTS auto_create_partition_for_year();

-- ============================================================================
-- PARTE 3: Drop Partition Creation Function
-- ============================================================================

DROP FUNCTION IF EXISTS create_missing_year_partitions(TEXT);

-- ============================================================================
-- PARTE 4: Drop Future Partition Tables (if they were created)
-- ============================================================================

DROP TABLE IF EXISTS catalogo_geometrias_particionada_2029;
DROP TABLE IF EXISTS catalogo_geometrias_particionada_2030;
DROP TABLE IF EXISTS catalogo_geometrias_particionada_2031;
DROP TABLE IF EXISTS catalogo_geometrias_particionada_2032;
DROP TABLE IF EXISTS catalogo_geometrias_particionada_2033;
DROP TABLE IF EXISTS catalogo_geometrias_particionada_2034;
DROP TABLE IF EXISTS catalogo_geometrias_particionada_2035;

-- ============================================================================
-- PARTE 5: Verification & Logging
-- ============================================================================

INSERT INTO audit_log (action, table_name, description, status, executed_at)
VALUES (
    'ROLLBACK',
    'catalogo_geometrias_particionada',
    'OPT4 Rollback: Removed auto-partition creation functions and trigger (2029+)',
    'SUCCESS',
    CURRENT_TIMESTAMP
)
ON CONFLICT DO NOTHING;

COMMIT;

-- ============================================================================
-- ROLLBACK VERIFICATION QUERIES
-- ============================================================================

-- Verify trigger is dropped
-- SELECT count(*) FROM pg_trigger 
-- WHERE tgname = 'trigger_auto_create_partition';
-- Expected: 0 rows

-- Verify functions are dropped
-- SELECT count(*) FROM pg_proc 
-- WHERE proname IN ('auto_create_partition_for_year', 'create_missing_year_partitions');
-- Expected: 0 rows

-- Verify future partitions are dropped
-- SELECT count(*) FROM information_schema.tables 
-- WHERE table_name LIKE 'catalogo_geometrias_particionada_202[9-9]%'
-- OR table_name LIKE 'catalogo_geometrias_particionada_203[0-5]%';
-- Expected: 0 rows
