-- ROLLBACK SCRIPT: OPT5 - MV Refresh Scheduling (Cron Automation)
-- Purpose: Reverse the CRON scheduling structures created in OPT5
-- Created: 2026-02-06
-- Status: STAGE 3 - Rollback Validation

BEGIN;

-- ============================================================================
-- PARTE 1: Unschedule CRON Jobs
-- ============================================================================

-- Unschedule hourly refresh
SELECT cron.unschedule('refresh-mv-stats-hourly');

-- Unschedule 30-minute refresh
SELECT cron.unschedule('refresh-mv-search-30min');

-- Unschedule nightly full refresh
SELECT cron.unschedule('refresh-mv-full-night');

-- ============================================================================
-- PARTE 2: Drop Batch Refresh Function
-- ============================================================================

DROP FUNCTION IF EXISTS refresh_all_materialized_views();

-- ============================================================================
-- PARTE 3: Drop Audit Log Indexes
-- ============================================================================

DROP INDEX IF EXISTS idx_mv_refresh_log_view_name;
DROP INDEX IF EXISTS idx_mv_refresh_log_status;

-- ============================================================================
-- PARTE 4: Drop Audit Log Table
-- ============================================================================

DROP TABLE IF EXISTS mv_refresh_log;

-- ============================================================================
-- PARTE 5: Verification & Logging
-- ============================================================================

INSERT INTO audit_log (action, table_name, description, status, executed_at)
VALUES (
    'ROLLBACK',
    'mv_refresh_log, pg_cron',
    'OPT5 Rollback: Removed CRON scheduling and MV refresh logging infrastructure',
    'SUCCESS',
    CURRENT_TIMESTAMP
)
ON CONFLICT DO NOTHING;

COMMIT;

-- ============================================================================
-- ROLLBACK VERIFICATION QUERIES
-- ============================================================================

-- Verify CRON jobs are unscheduled
-- SELECT count(*) FROM cron.job 
-- WHERE jobname IN ('refresh-mv-stats-hourly', 'refresh-mv-search-30min', 'refresh-mv-full-night');
-- Expected: 0 rows

-- Verify function is dropped
-- SELECT count(*) FROM pg_proc 
-- WHERE proname = 'refresh_all_materialized_views';
-- Expected: 0 rows

-- Verify audit log table is dropped
-- SELECT count(*) FROM information_schema.tables 
-- WHERE table_name = 'mv_refresh_log';
-- Expected: 0 rows

-- Note: pg_cron extension itself remains installed (not dropped)
-- To fully remove pg_cron extension, use: DROP EXTENSION pg_cron;
