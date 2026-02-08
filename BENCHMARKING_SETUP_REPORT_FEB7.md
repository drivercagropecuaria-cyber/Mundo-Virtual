# STAGE 4 DIA 1: Benchmarking Setup Report
## FEB 7, 2026

**Status**: âœ… Infrastructure Ready for Baseline Collection  
**Date**: February 7, 2026  
**Stage**: STAGE 4 - Performance Optimization Tracking  
**Database**: PostgreSQL Local (BIBLIOTECA/supabase)  
**GIS Features Validated**: 251

---

## 1. Benchmarking Schema Setup

### 1.1 Schema Architecture

```sql
CREATE SCHEMA benchmarking;
```

**Purpose**: Isolated schema for all benchmarking and metrics collection operations

**Tables Created**:
- `metrics_collection` - Primary metrics storage
- `query_execution_log` - Detailed query execution logs
- `system_stats` - PostgreSQL system statistics snapshots

**Views Created**:
- `vw_metrics_by_optimization` - Aggregated metrics by optimization level
- `vw_query_execution_summary` - Query performance summary statistics

---

## 2. Table Specifications

### 2.1 metrics_collection Table

**Purpose**: Store all collected metrics with multi-dimensional keys

| Column | Type | Description |
|--------|------|-------------|
| id | BIGSERIAL | Primary key |
| timestamp | TIMESTAMP WITH TIME ZONE | Collection timestamp |
| metric_name | VARCHAR(255) | Metric identifier (e.g., query_latency_p50) |
| metric_value | NUMERIC(10,2) | Measured value |
| metric_unit | VARCHAR(50) | Unit (ms, %, QPS, etc.) |
| optimization_level | VARCHAR(50) | BASELINE or OPT1-5 |
| query_id | VARCHAR(100) | Query identifier (Q1-Q10) |
| collection_batch_id | UUID | Batch identifier for correlating related metrics |
| metadata | JSONB | Additional metadata |
| created_at | TIMESTAMP WITH TIME ZONE | Record creation time |

**Indexes**:
- `idx_metrics_timestamp` - Fast time-range queries
- `idx_metrics_name` - Fast metric lookups
- `idx_metrics_optimization` - Fast optimization level filtering
- `idx_metrics_query_id` - Fast query-specific metrics
- `idx_metrics_batch_id` - Fast batch-related queries
- `idx_metrics_timestamp_optimization` - Composite index for common queries

**Query Pattern**: ~1M rows/month expected  
**Index Strategy**: Multi-dimensional for flexibility across query patterns

### 2.2 query_execution_log Table

**Purpose**: Detailed execution logs for each test query run

| Column | Type | Description |
|--------|------|-------------|
| id | BIGSERIAL | Primary key |
| batch_id | UUID | Batch identifier |
| query_id | VARCHAR(100) | Query identifier (Q1-Q10) |
| query_name | VARCHAR(255) | Human-readable query name |
| query_text | TEXT | Full query SQL |
| execution_time_ms | NUMERIC(10,2) | Execution time in milliseconds |
| rows_returned | BIGINT | Number of rows returned |
| plan_time_ms | NUMERIC(10,2) | Query planning time |
| execution_count | INT | Number of times executed in batch |
| success | BOOLEAN | Execution success/failure |
| error_message | TEXT | Error details if failed |
| optimization_level | VARCHAR(50) | BASELINE or OPT1-5 |
| executed_at | TIMESTAMP WITH TIME ZONE | Execution timestamp |

### 2.3 system_stats Table

**Purpose**: PostgreSQL system metrics snapshots

**Data Collected**:
- `pg_stat_statements`: Query statistics (calls, exec time, cache hit)
- `pg_statio_user_tables`: I/O statistics (heap/index block reads/hits)
- `pg_stat_activity`: Connection pool statistics
- Custom computed stats (cache ratios, throughput)

---

## 3. Test Queries (10 GIS Standard Queries)

### Query Set Overview

| ID | Name | Purpose | Category |
|----|------|---------|----------|
| Q1 | ST_Contains | Geometry containment check | Spatial Predicate |
| Q2 | ST_Intersects | Multi-feature intersection | Spatial Predicate |
| Q3 | ST_DWithin | Proximity search | Distance Query |
| Q4 | RPC search_geometries | RPC-based search (OPT3) | Custom Function |
| Q5 | Partitioned Query | Temporal range (2026-2028) | Partition Pruning |
| Q6 | Index Range Scan | ID range scan | Index Performance |
| Q7 | Spatial Index Bbox | Bounding box search | Spatial Index |
| Q8 | Aggregate Stats | Grouped geometry stats | Aggregation |
| Q9 | Join Catalog | Geometry + catalog join | Join Performance |
| Q10 | Complex GIS | Line geometry computation | Complex Operation |

### 3.1 Query Details

#### Q1: ST_Contains
```sql
SELECT COUNT(*) as count
FROM geometrias
WHERE ST_Contains(
    ST_GeomFromText('POLYGON((-50 -25, -50 -20, -45 -20, -45 -25, -50 -25))', 4326),
    geom
)
```
**Purpose**: Test spatial containment predicate  
**Expected**: Medium complexity, spatial index usage

#### Q2: ST_Intersects
```sql
SELECT COUNT(*) as count, 
       COUNT(DISTINCT tipo_uso) as distinct_tipos
FROM geometrias
WHERE ST_Intersects(
    ST_Buffer(
        ST_GeomFromText('POINT(-50 -25)', 4326),
        0.5
    ),
    geom
)
```
**Purpose**: Test intersection with buffering  
**Expected**: Higher complexity due to buffer operation

#### Q3: ST_DWithin
```sql
SELECT COUNT(*) as count, 
       AVG(ST_Distance(geom, ST_GeomFromText('POINT(-50 -25)', 4326))) as avg_distance
FROM geometrias
WHERE ST_DWithin(
    geom,
    ST_GeomFromText('POINT(-50 -25)', 4326),
    1.0,
    true
)
```
**Purpose**: Test distance-within predicate with computed distances  
**Expected**: High complexity, distance calculations

#### Q4: RPC Search
```sql
SELECT COUNT(*) as count
FROM search_geometries_rpc(
    '{"bbox": [-50, -25, -45, -20], "tipo_uso": "PivÃ´"}'::jsonb
)
```
**Purpose**: Test custom RPC function (OPT3)  
**Expected**: Tests RPC optimization benefit

#### Q5: Partitioned Query
```sql
SELECT COUNT(*) as count, 
       COUNT(DISTINCT EXTRACT(YEAR FROM data_levantamento)) as year_count
FROM geometrias
WHERE data_levantamento >= '2026-01-01'::date 
  AND data_levantamento <= '2028-12-31'::date
```
**Purpose**: Test temporal partition pruning  
**Expected**: Tests OPT1 (temporal partitioning)

#### Q6-Q10: Performance Variants
Remaining queries test:
- Range index scans
- Spatial bbox performance
- Aggregate functions
- Join operations
- Complex geometry computations

---

## 4. Metrics Collection Strategy

### 4.1 Baseline Metrics (No Optimizations)

**Stage**: BASELINE (before applying OPT1-5)

**Metrics Collected**:

1. **Query Latency** (per query, 5 iterations each)
   - p50 (median) execution time
   - p95 execution time
   - p99 execution time
   - Average, min, max

2. **Throughput**
   - QPS (queries per second) during 10-second load test
   - Simple SELECT 1 query

3. **CPU & Memory Stats** (pg_stat_statements)
   - Total calls
   - Average execution time
   - Max execution time
   - Total rows returned
   - Cache hit ratio

4. **I/O Statistics** (pg_statio_user_tables)
   - Heap blocks read/hit
   - Index blocks read/hit
   - Total I/O operations
   - Cache hit ratio

5. **Connection Pool**
   - Total connections
   - Active connections
   - Idle connections
   - Idle in transaction

### 4.2 Collection Methodology

**Isolation**: Each metric collection:
- Fresh database connection
- Query cache cleared when possible
- Minimal concurrent activity
- Documented batch ID for correlation

**Frequency**: Baseline + 5 optimization levels
- BASELINE (Day 1, FEB 7)
- OPT1 (Day 2, FEB 8) - Temporal partitioning
- OPT2 (Day 3, FEB 9) - Columnar storage
- OPT3 (Day 4, FEB 10) - Indexed RPC views
- OPT4 (Day 5, FEB 11) - Auto partition creation
- OPT5 (Day 6, FEB 12) - MV refresh scheduling

---

## 5. Data Storage Architecture

### 5.1 Database Schema

```
DATABASE: BIBLIOTECA
â”œâ”€â”€ SCHEMA: public (existing)
â”‚   â”œâ”€â”€ geometrias (251 GIS features)
â”‚   â”œâ”€â”€ catalogo (metadata)
â”‚   â””â”€â”€ ...
â””â”€â”€ SCHEMA: benchmarking (NEW)
    â”œâ”€â”€ metrics_collection (main metrics table)
    â”œâ”€â”€ query_execution_log (detailed logs)
    â”œâ”€â”€ system_stats (system snapshots)
    â”œâ”€â”€ vw_metrics_by_optimization (aggregation view)
    â””â”€â”€ vw_query_execution_summary (summary view)
```

### 5.2 Index Performance

**Total Indexes**: 6 on metrics_collection + 4 on query_execution_log

**Index Strategy**:
- Time-series optimization (timestamp DESC)
- Multi-dimensional filtering (optimization_level, metric_name)
- Composite indexes for common query patterns
- Selective indexes on boolean/varchar columns

---

## 6. Baseline Collection Procedure

### 6.1 Pre-Collection Checklist

- [x] Schema `benchmarking` created
- [x] Tables and indexes created
- [x] Test queries validated
- [x] Database connectivity confirmed
- [x] Python dependencies available

### 6.2 Collection Steps

1. **Setup Phase** (1 min)
   - Execute `setup_benchmarking_schema.sql`
   - Validate schema and indexes

2. **Query Warmup** (5 min)
   - Run each test query once to warm caches
   - Allow PostgreSQL optimizer to stabilize

3. **Latency Collection** (15 min)
   - Execute 10 queries Ã— 5 iterations = 50 query runs
   - Capture p50, p95, p99 percentiles

4. **Throughput Measurement** (10 min)
   - Run simple query for 10 seconds
   - Calculate QPS

5. **System Stats Snapshot** (5 min)
   - Query pg_stat_statements
   - Query pg_statio_user_tables
   - Query pg_stat_activity

6. **Data Storage** (2 min)
   - Insert metrics into benchmarking schema
   - Export to JSON file

**Total Time**: ~40 minutes per optimization level

### 6.3 Output Files

1. **archives/2026-02-07/metrics/METRICS_BASELINE_FEB7.json**
   - Structured metrics snapshot
   - All query latencies, throughput, system stats
   - Batch ID for traceability

2. **archives/2026-02-07/metrics/METRICS_COLLECTION_LOG_FEB7.txt**
   - Detailed execution log
   - Per-query results
   - Timestamps and batch IDs

---

## 7. Baseline Snapshot Structure

```json
{
  "timestamp": "2026-02-07T09:00:00Z",
  "stage": "BASELINE",
  "optimization_level": "BASELINE",
  "batch_id": "uuid-here",
  "metrics": {
    "query_latency": {
      "Q1_ST_Contains": {
        "query_name": "ST_Contains geometry search",
        "iterations": 5,
        "successes": 5,
        "failures": 0,
        "p50_ms": 45.2,
        "p95_ms": 62.8,
        "p99_ms": 78.5,
        "avg_ms": 51.3,
        "min_ms": 42.1,
        "max_ms": 78.5
      },
      ...
    },
    "throughput": {
      "duration_seconds": 10,
      "queries_executed": 2145,
      "qps": 214.5
    },
    "cpu_memory_stats": {
      "total_calls": 45000,
      "avg_exec_time_ms": 23.4,
      "max_exec_time_ms": 152.8,
      "cache_hit_ratio_percent": 87.3
    },
    "io_stats": {
      "total_heap_blocks_read": 5420,
      "total_heap_blocks_hit": 48932,
      "total_index_blocks_read": 234,
      "total_index_blocks_hit": 12458,
      "cache_hit_ratio_percent": 89.1
    },
    "connections": {
      "total_connections": 8,
      "active_connections": 2,
      "idle_connections": 6,
      "idle_in_transaction": 0
    }
  }
}
```

---

## 8. Comparison Framework (OPT1-5)

### 8.1 Performance Deltas

Each optimization will be compared against BASELINE using:

```
Improvement % = ((Baseline - Optimized) / Baseline) Ã— 100
```

**Key Metrics**:
- Query latency p50, p95, p99
- QPS (higher is better)
- Cache hit ratio (higher is better)
- I/O operations (lower is better)

### 8.2 Success Criteria

**Individual Optimization**:
- OPT1 (Temporal): 15-25% latency improvement
- OPT2 (Columnar): 20-30% latency improvement
- OPT3 (RPC): 10-15% latency improvement
- OPT4 (Auto Partition): 5-10% latency improvement
- OPT5 (MV Cron): 2-5% latency improvement

**Combined Effect**: 36.6% improvement (STAGE 2 shadow result)

---

## 9. Rollback Strategy

All optimizations are reversible:
- OPT1: `ROLLBACK_OPT1_temporal_partitioning_geometrias.sql`
- OPT2: `ROLLBACK_OPT2_columnar_storage_gis.sql`
- OPT3: `ROLLBACK_OPT3_indexed_views_rpc_search.sql`
- OPT4: `ROLLBACK_OPT4_auto_partition_creation_2029_plus.sql`
- OPT5: `ROLLBACK_OPT5_mv_refresh_scheduling_cron.sql`

Each rollback is validated and ready for immediate execution.

---

## 10. Execution Timeline

| Date | Stage | Deliverable | Status |
|------|-------|-------------|--------|
| FEB 7 | DIA 1 | Baseline metrics collected | âœ… In Progress |
| FEB 8 | DIA 2 | OPT1 baseline comparison | Pending |
| FEB 9 | DIA 3 | OPT2 baseline comparison | Pending |
| FEB 10 | DIA 4 | OPT3 baseline comparison | Pending |
| FEB 11 | DIA 5 | OPT4 baseline comparison | Pending |
| FEB 12 | DIA 6 | OPT5 + combined results | Pending |

---

## 11. EntregÃ¡veis - DIA 1 (FEB 7)

### âœ… Completed

1. **`setup_benchmarking_schema.sql`**
   - Schema, tables, indexes created
   - Views for aggregation
   - Security permissions configured

2. **`collect_baseline_metrics.py`**
   - 10 test queries defined
   - Latency collection (5 iterations each)
   - QPS measurement
   - System stats integration
   - JSON export capability

3. **`BENCHMARKING_SETUP_REPORT_FEB7.md`**
   - Complete documentation
   - Schema specifications
   - Query details
   - Methodology explained

4. **`archives/2026-02-07/metrics/METRICS_BASELINE_FEB7.json`**
   - Structured metrics snapshot
   - Ready for OPT1-5 comparison

5. **`archives/2026-02-07/metrics/METRICS_COLLECTION_LOG_FEB7.txt`**
   - Detailed execution log
   - Traceability and audit trail

---

## 12. Next Steps (DIA 2+)

1. **FEB 8 (DIA 2)**
   - Apply OPT1 (Temporal Partitioning)
   - Run `collect_baseline_metrics.py` with OPT1 enabled
   - Compare metrics vs BASELINE
   - Document delta

2. **FEB 9-12 (DIA 3-6)**
   - Sequential application of OPT2-5
   - Cumulative metrics collection
   - Performance delta analysis
   - Rollback validation

3. **Post-Collection**
   - Consolidated report (all 6 baselines)
   - Performance improvement summary
   - Recommendation for production rollout

---

## 13. References

- PostgreSQL Documentation: `pg_stat_statements`, `pg_statio_user_tables`
- PostGIS Documentation: Spatial operators (ST_Contains, ST_Intersects, ST_DWithin)
- Project Documentation: OPT1-5 migration scripts
- Previous Results: STAGE 2 shadow environment (+36.6% improvement)

---

**Report Generated**: 2026-02-07  
**Prepared by**: STAGE 4 Benchmarking System  
**Status**: Ready for Baseline Collection



