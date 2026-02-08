-- ============================================================================
-- STAGE 4 DIA 1: Setup Benchmarking Infrastructure
-- Date: FEB 7, 2026
-- Purpose: Create benchmarking schema and tables for baseline metrics collection
-- ============================================================================

-- Create schema if not exists
CREATE SCHEMA IF NOT EXISTS benchmarking;

-- Drop existing tables if they exist (fresh start)
DROP TABLE IF EXISTS benchmarking.metrics_collection CASCADE;
DROP TABLE IF EXISTS benchmarking.query_execution_log CASCADE;
DROP TABLE IF EXISTS benchmarking.system_stats CASCADE;

-- ============================================================================
-- Table 1: metrics_collection
-- Stores collected metrics for all optimization levels
-- ============================================================================
CREATE TABLE benchmarking.metrics_collection (
    id BIGSERIAL PRIMARY KEY,
    timestamp TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    metric_name VARCHAR(255) NOT NULL,
    metric_value NUMERIC(10, 2),
    metric_unit VARCHAR(50),
    optimization_level VARCHAR(50),
    query_id VARCHAR(100),
    collection_batch_id UUID,
    metadata JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create indexes for fast queries
CREATE INDEX idx_metrics_timestamp ON benchmarking.metrics_collection(timestamp DESC);
CREATE INDEX idx_metrics_name ON benchmarking.metrics_collection(metric_name);
CREATE INDEX idx_metrics_optimization ON benchmarking.metrics_collection(optimization_level);
CREATE INDEX idx_metrics_query_id ON benchmarking.metrics_collection(query_id);
CREATE INDEX idx_metrics_batch_id ON benchmarking.metrics_collection(collection_batch_id);
CREATE INDEX idx_metrics_timestamp_optimization ON benchmarking.metrics_collection(timestamp DESC, optimization_level);

-- ============================================================================
-- Table 2: query_execution_log
-- Detailed logs for each query execution
-- ============================================================================
CREATE TABLE benchmarking.query_execution_log (
    id BIGSERIAL PRIMARY KEY,
    batch_id UUID NOT NULL,
    query_id VARCHAR(100) NOT NULL,
    query_name VARCHAR(255),
    query_text TEXT,
    execution_time_ms NUMERIC(10, 2),
    rows_returned BIGINT,
    plan_time_ms NUMERIC(10, 2),
    execution_count INT DEFAULT 1,
    success BOOLEAN,
    error_message TEXT,
    optimization_level VARCHAR(50),
    executed_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create indexes for query execution log
CREATE INDEX idx_query_exec_batch ON benchmarking.query_execution_log(batch_id);
CREATE INDEX idx_query_exec_query_id ON benchmarking.query_execution_log(query_id);
CREATE INDEX idx_query_exec_time ON benchmarking.query_execution_log(executed_at DESC);
CREATE INDEX idx_query_exec_optimization ON benchmarking.query_execution_log(optimization_level);

-- ============================================================================
-- Table 3: system_stats
-- PostgreSQL system statistics snapshots
-- ============================================================================
CREATE TABLE benchmarking.system_stats (
    id BIGSERIAL PRIMARY KEY,
    batch_id UUID NOT NULL,
    snapshot_time TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    stat_type VARCHAR(100),
    stat_name VARCHAR(255),
    stat_value NUMERIC(15, 2),
    stat_unit VARCHAR(50),
    optimization_level VARCHAR(50),
    database_name VARCHAR(100),
    table_name VARCHAR(100),
    metadata JSONB
);

-- Create indexes for system stats
CREATE INDEX idx_system_stats_batch ON benchmarking.system_stats(batch_id);
CREATE INDEX idx_system_stats_type ON benchmarking.system_stats(stat_type);
CREATE INDEX idx_system_stats_time ON benchmarking.system_stats(snapshot_time DESC);
CREATE INDEX idx_system_stats_optimization ON benchmarking.system_stats(optimization_level);

-- ============================================================================
-- Views for easy metric aggregation
-- ============================================================================

-- View: Average metrics by optimization level
CREATE OR REPLACE VIEW benchmarking.vw_metrics_by_optimization AS
SELECT 
    optimization_level,
    metric_name,
    AVG(metric_value) as avg_value,
    MIN(metric_value) as min_value,
    MAX(metric_value) as max_value,
    STDDEV(metric_value) as stddev_value,
    COUNT(*) as measurement_count,
    MAX(timestamp) as latest_timestamp
FROM benchmarking.metrics_collection
WHERE metric_value IS NOT NULL
GROUP BY optimization_level, metric_name
ORDER BY optimization_level, metric_name;

-- View: Query execution summary
CREATE OR REPLACE VIEW benchmarking.vw_query_execution_summary AS
SELECT 
    query_id,
    query_name,
    optimization_level,
    COUNT(*) as execution_count,
    AVG(execution_time_ms) as avg_execution_time_ms,
    PERCENTILE_CONT(0.50) WITHIN GROUP (ORDER BY execution_time_ms) as p50_execution_time_ms,
    PERCENTILE_CONT(0.95) WITHIN GROUP (ORDER BY execution_time_ms) as p95_execution_time_ms,
    PERCENTILE_CONT(0.99) WITHIN GROUP (ORDER BY execution_time_ms) as p99_execution_time_ms,
    MIN(execution_time_ms) as min_execution_time_ms,
    MAX(execution_time_ms) as max_execution_time_ms,
    SUM(CASE WHEN success = true THEN 1 ELSE 0 END) as successful_executions,
    SUM(CASE WHEN success = false THEN 1 ELSE 0 END) as failed_executions
FROM benchmarking.query_execution_log
GROUP BY query_id, query_name, optimization_level
ORDER BY query_id, optimization_level;

-- ============================================================================
-- Security: Grant permissions
-- ============================================================================
GRANT USAGE ON SCHEMA benchmarking TO postgres;
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA benchmarking TO postgres;
GRANT EXECUTE ON ALL FUNCTIONS IN SCHEMA benchmarking TO postgres;
GRANT SELECT ON ALL TABLES IN SCHEMA benchmarking TO postgres;

-- ============================================================================
-- Validation: Schema setup complete
-- ============================================================================
SELECT 
    'benchmarking' as schema_name,
    COUNT(*) as table_count,
    NOW() as created_at
FROM information_schema.tables 
WHERE table_schema = 'benchmarking'
GROUP BY schema_name;
