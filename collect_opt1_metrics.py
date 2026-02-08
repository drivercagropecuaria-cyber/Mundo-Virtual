#!/usr/bin/env python3
"""
STAGE 4 DIA 2: OPT1 Metrics Collection
Date: FEB 7, 2026 (Same day continuation)
Optimization: OPT1 - Temporal Partitioning (geometrias)
Purpose: Measure performance improvement with OPT1 applied

Expected improvement: 15-25% latency reduction
Target queries: Q5 (2026-2028 partition pruning)
"""

import psycopg2
import json
import time
import statistics
import uuid
from datetime import datetime
from typing import Dict, List, Tuple, Any
import logging
import os

# ============================================================================
# Configuration
# ============================================================================

DB_CONFIG = {
    'host': os.environ.get('DB_HOST', 'localhost'),
    'port': int(os.environ.get('DB_PORT', '5432')),
    'database': os.environ.get('DB_NAME', 'BIBLIOTECA'),
    'user': os.environ.get('DB_USER', 'postgres'),
    'password': os.environ.get('DB_PASSWORD', 'postgres')
}

LOG_FILE = 'archives/2026-02-07/metrics/METRICS_COLLECTION_LOG_OPT1_FEB7.txt'
METRICS_OUTPUT = 'archives/2026-02-07/metrics/METRICS_OPT1_FEB7.json'
BASELINE_METRICS = 'archives/2026-02-07/metrics/METRICS_BASELINE_FEB7.json'
BATCH_ID = str(uuid.uuid4())
OPTIMIZATION_LEVEL = 'OPT1'

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# ============================================================================
# Test Queries - Same 10 GIS Queries (Now with OPT1)
# ============================================================================

TEST_QUERIES = {
    'Q1_ST_Contains': {
        'name': 'ST_Contains geometry search',
        'query': '''
            SELECT COUNT(*) as count
            FROM geometrias
            WHERE ST_Contains(
                ST_GeomFromText('POLYGON((-50 -25, -50 -20, -45 -20, -45 -25, -50 -25))', 4326),
                geom
            )
        '''
    },
    'Q2_ST_Intersects': {
        'name': 'ST_Intersects multi-feature',
        'query': '''
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
        '''
    },
    'Q3_ST_DWithin': {
        'name': 'ST_DWithin proximity search',
        'query': '''
            SELECT COUNT(*) as count, 
                   AVG(ST_Distance(geom, ST_GeomFromText('POINT(-50 -25)', 4326))) as avg_distance
            FROM geometrias
            WHERE ST_DWithin(
                geom,
                ST_GeomFromText('POINT(-50 -25)', 4326),
                1.0,
                true
            )
        '''
    },
    'Q4_RPC_Search': {
        'name': 'RPC search_geometries (OPT3)',
        'query': '''
            SELECT COUNT(*) as count
            FROM search_geometries_rpc(
                '{"bbox": [-50, -25, -45, -20], "tipo_uso": "PivÃ´"}'::jsonb
            )
        '''
    },
    'Q5_Partitioned': {
        'name': 'Partitioned query (2026-2028 range) - OPT1 TARGET',
        'query': '''
            SELECT COUNT(*) as count, 
                   COUNT(DISTINCT EXTRACT(YEAR FROM data_levantamento)) as year_count
            FROM geometrias
            WHERE data_levantamento >= '2026-01-01'::date 
              AND data_levantamento <= '2028-12-31'::date
        '''
    },
    'Q6_Index_Range': {
        'name': 'Index range scan',
        'query': '''
            SELECT COUNT(*) as count
            FROM geometrias
            WHERE id_catalogo >= 1000 AND id_catalogo <= 2000
        '''
    },
    'Q7_Spatial_Index': {
        'name': 'Spatial index bbox search',
        'query': '''
            SELECT COUNT(*) as count
            FROM geometrias
            WHERE geom && ST_MakeBox2D(
                ST_Point(-50, -25),
                ST_Point(-45, -20)
            )
        '''
    },
    'Q8_Aggregate_Stats': {
        'name': 'Aggregate with spatial stats',
        'query': '''
            SELECT tipo_uso, 
                   COUNT(*) as feature_count,
                   AVG(ST_Area(geom)) as avg_area,
                   MIN(ST_Area(geom)) as min_area,
                   MAX(ST_Area(geom)) as max_area
            FROM geometrias
            WHERE ST_Area(geom) > 0
            GROUP BY tipo_uso
            HAVING COUNT(*) > 10
        '''
    },
    'Q9_Join_Catalog': {
        'name': 'Join with catalog metadata',
        'query': '''
            SELECT COUNT(*) as count
            FROM geometrias g
            INNER JOIN catalogo c ON g.id_catalogo = c.id
            WHERE c.status = 'ATIVO'
              AND g.geom IS NOT NULL
            LIMIT 1000
        '''
    },
    'Q10_Complex_GIS': {
        'name': 'Complex GIS computation',
        'query': '''
            SELECT COUNT(*) as count,
                   PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY ST_Length(geom)) as median_length,
                   MAX(ST_NPoints(geom)) as max_points
            FROM geometrias
            WHERE ST_GeometryType(geom) IN ('ST_LineString', 'ST_LinearRing')
              AND ST_Length(geom) > 0
        '''
    }
}

# ============================================================================
# Helper Functions
# ============================================================================

def connect_db():
    """Establish PostgreSQL connection"""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        logger.info(f"Connected to PostgreSQL: {DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}")
        return conn
    except Exception as e:
        logger.error(f"Failed to connect to database: {str(e)}")
        raise

def execute_query(conn, query: str, timeout: int = 300) -> Tuple[float, int, bool, str]:
    """Execute query and measure execution time"""
    try:
        cursor = conn.cursor()
        cursor.execute(f"SET statement_timeout TO {timeout * 1000}")
        
        start_time = time.perf_counter()
        cursor.execute(query)
        end_time = time.perf_counter()
        
        rows_count = cursor.rowcount if cursor.rowcount >= 0 else len(cursor.fetchall())
        execution_time_ms = (end_time - start_time) * 1000
        
        cursor.close()
        return execution_time_ms, rows_count, True, ""
    except Exception as e:
        logger.error(f"Query execution failed: {str(e)}")
        return 0, 0, False, str(e)

def collect_query_latency(conn) -> Dict[str, Any]:
    """Collect latency metrics for 10 test queries with OPT1"""
    logger.info("=" * 80)
    logger.info("COLLECTING QUERY LATENCY METRICS (OPT1)")
    logger.info("=" * 80)
    
    latency_results = {}
    
    for query_id, query_info in TEST_QUERIES.items():
        logger.info(f"\nExecuting {query_id}: {query_info['name']}")
        
        execution_times = []
        successes = 0
        failures = 0
        
        # Run each query 5 times
        for iteration in range(5):
            exec_time, rows, success, error = execute_query(conn, query_info['query'])
            
            if success:
                execution_times.append(exec_time)
                successes += 1
                logger.info(f"  Iteration {iteration + 1}: {exec_time:.2f}ms (rows: {rows})")
            else:
                failures += 1
                logger.error(f"  Iteration {iteration + 1}: FAILED - {error}")
        
        if execution_times:
            latency_results[query_id] = {
                'query_name': query_info['name'],
                'iterations': 5,
                'successes': successes,
                'failures': failures,
                'p50_ms': statistics.median(execution_times),
                'p95_ms': sorted(execution_times)[int(len(execution_times) * 0.95)] if len(execution_times) > 1 else execution_times[0],
                'p99_ms': sorted(execution_times)[int(len(execution_times) * 0.99)] if len(execution_times) > 1 else execution_times[0],
                'avg_ms': statistics.mean(execution_times),
                'min_ms': min(execution_times),
                'max_ms': max(execution_times)
            }
    
    return latency_results

def collect_throughput(conn) -> Dict[str, Any]:
    """Collect QPS metrics with OPT1"""
    logger.info("\n" + "=" * 80)
    logger.info("COLLECTING THROUGHPUT METRICS (QPS) - OPT1")
    logger.info("=" * 80)
    
    simple_query = "SELECT 1;"
    duration_seconds = 10
    query_count = 0
    start_time = time.perf_counter()
    
    try:
        cursor = conn.cursor()
        while time.perf_counter() - start_time < duration_seconds:
            cursor.execute(simple_query)
            query_count += 1
        cursor.close()
    except Exception as e:
        logger.error(f"Throughput test failed: {str(e)}")
    
    elapsed = time.perf_counter() - start_time
    qps = query_count / elapsed if elapsed > 0 else 0
    
    logger.info(f"Queries executed: {query_count}")
    logger.info(f"Elapsed time: {elapsed:.2f}s")
    logger.info(f"QPS: {qps:.2f}")
    
    return {
        'duration_seconds': duration_seconds,
        'queries_executed': query_count,
        'qps': qps
    }

def collect_cpu_memory_stats(conn) -> Dict[str, Any]:
    """Collect CPU and Memory stats (OPT1)"""
    logger.info("\n" + "=" * 80)
    logger.info("COLLECTING CPU & MEMORY STATS (OPT1)")
    logger.info("=" * 80)
    
    stats = {}
    try:
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT EXISTS (
                SELECT 1 FROM pg_extension WHERE extname = 'pg_stat_statements'
            );
        """)
        ext_exists = cursor.fetchone()[0]
        
        if ext_exists:
            cursor.execute("""
                SELECT 
                    SUM(calls) as total_calls,
                    AVG(mean_exec_time) as avg_exec_time_ms,
                    MAX(max_exec_time) as max_exec_time_ms,
                    SUM(rows) as total_rows_returned,
                    SUM(100 * shared_blks_hit / NULLIF(shared_blks_hit + shared_blks_read, 0)) as cache_hit_ratio
                FROM pg_stat_statements
                WHERE query NOT LIKE '%pg_stat_statements%'
            """)
            
            result = cursor.fetchone()
            if result:
                stats = {
                    'total_calls': result[0] or 0,
                    'avg_exec_time_ms': result[1] or 0,
                    'max_exec_time_ms': result[2] or 0,
                    'total_rows_returned': result[3] or 0,
                    'cache_hit_ratio_percent': result[4] or 0
                }
                logger.info(f"Total calls: {stats['total_calls']}")
                logger.info(f"Avg exec time: {stats['avg_exec_time_ms']:.2f}ms")
                logger.info(f"Cache hit ratio: {stats['cache_hit_ratio_percent']:.2f}%")
        else:
            logger.warning("pg_stat_statements extension not available")
            stats = {'available': False}
        
        cursor.close()
    except Exception as e:
        logger.error(f"Failed to collect pg_stat_statements: {str(e)}")
        stats = {'error': str(e)}
    
    return stats

def collect_io_stats(conn) -> Dict[str, Any]:
    """Collect I/O stats (OPT1)"""
    logger.info("\n" + "=" * 80)
    logger.info("COLLECTING I/O STATS (OPT1)")
    logger.info("=" * 80)
    
    stats = {}
    try:
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT 
                schemaname,
                tablename,
                heap_blks_read,
                heap_blks_hit,
                idx_blks_read,
                idx_blks_hit,
                toast_blks_read,
                toast_blks_hit
            FROM pg_statio_user_tables
            WHERE schemaname NOT IN ('pg_catalog', 'information_schema')
            ORDER BY heap_blks_read + heap_blks_hit DESC
            LIMIT 10
        """)
        
        tables_io = cursor.fetchall()
        total_heap_read = 0
        total_heap_hit = 0
        total_idx_read = 0
        total_idx_hit = 0
        
        for row in tables_io:
            schema, table, heap_read, heap_hit, idx_read, idx_hit, toast_read, toast_hit = row
            total_heap_read += heap_read
            total_heap_hit += heap_hit
            total_idx_read += idx_read
            total_idx_hit += idx_hit
        
        total_io = total_heap_read + total_heap_hit + total_idx_read + total_idx_hit
        stats = {
            'total_heap_blocks_read': total_heap_read,
            'total_heap_blocks_hit': total_heap_hit,
            'total_index_blocks_read': total_idx_read,
            'total_index_blocks_hit': total_idx_hit,
            'total_io_operations': total_io,
            'cache_hit_ratio_percent': (total_heap_hit + total_idx_hit) / total_io * 100 if total_io > 0 else 0,
            'tables_sampled': len(tables_io)
        }
        
        logger.info(f"Heap blocks (read/hit): {total_heap_read}/{total_heap_hit}")
        logger.info(f"Index blocks (read/hit): {total_idx_read}/{total_idx_hit}")
        logger.info(f"Overall I/O cache hit: {stats['cache_hit_ratio_percent']:.2f}%")
        
        cursor.close()
    except Exception as e:
        logger.error(f"Failed to collect I/O stats: {str(e)}")
        stats = {'error': str(e)}
    
    return stats

def collect_connection_count(conn) -> Dict[str, Any]:
    """Collect connection statistics"""
    logger.info("\n" + "=" * 80)
    logger.info("COLLECTING CONNECTION METRICS")
    logger.info("=" * 80)
    
    stats = {}
    try:
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT 
                COUNT(*) as total_connections,
                COUNT(*) FILTER (WHERE state = 'active') as active_connections,
                COUNT(*) FILTER (WHERE state = 'idle') as idle_connections,
                COUNT(*) FILTER (WHERE state = 'idle in transaction') as idle_in_transaction
            FROM pg_stat_activity
            WHERE datname = current_database()
        """)
        
        result = cursor.fetchone()
        if result:
            stats = {
                'total_connections': result[0],
                'active_connections': result[1],
                'idle_connections': result[2],
                'idle_in_transaction': result[3]
            }
            logger.info(f"Total connections: {stats['total_connections']}")
            logger.info(f"Active: {stats['active_connections']}, Idle: {stats['idle_connections']}")
        
        cursor.close()
    except Exception as e:
        logger.error(f"Failed to collect connection stats: {str(e)}")
        stats = {'error': str(e)}
    
    return stats

def load_baseline_metrics() -> Dict[str, Any]:
    """Load baseline metrics for comparison"""
    try:
        with open(BASELINE_METRICS, 'r') as f:
            return json.load(f)
    except Exception as e:
        logger.warning(f"Could not load baseline metrics: {str(e)}")
        return {}

def calculate_deltas(baseline: Dict, opt1: Dict) -> Dict[str, Any]:
    """Calculate improvement deltas vs baseline"""
    deltas = {}
    
    try:
        # Query latency deltas
        deltas['query_latency_deltas'] = {}
        baseline_latency = baseline.get('metrics', {}).get('query_latency', {})
        opt1_latency = opt1.get('metrics', {}).get('query_latency', {})
        
        for query_id in opt1_latency:
            if query_id in baseline_latency:
                baseline_p50 = baseline_latency[query_id].get('p50_ms', 0)
                opt1_p50 = opt1_latency[query_id].get('p50_ms', 0)
                
                if baseline_p50 > 0:
                    improvement = ((baseline_p50 - opt1_p50) / baseline_p50) * 100
                    deltas['query_latency_deltas'][query_id] = {
                        'baseline_p50_ms': baseline_p50,
                        'opt1_p50_ms': opt1_p50,
                        'improvement_percent': improvement,
                        'improvement_ms': baseline_p50 - opt1_p50
                    }
        
        # Throughput delta
        baseline_qps = baseline.get('metrics', {}).get('throughput', {}).get('qps', 0)
        opt1_qps = opt1.get('metrics', {}).get('throughput', {}).get('qps', 0)
        if baseline_qps > 0:
            deltas['throughput_improvement_percent'] = ((opt1_qps - baseline_qps) / baseline_qps) * 100
        
    except Exception as e:
        logger.warning(f"Could not calculate deltas: {str(e)}")
    
    return deltas

def save_metrics_to_json(metrics_data: Dict[str, Any], deltas: Dict[str, Any]):
    """Save OPT1 metrics to JSON file"""
    logger.info("\n" + "=" * 80)
    logger.info("SAVING OPT1 METRICS TO JSON")
    logger.info("=" * 80)
    
    output = {
        'timestamp': datetime.utcnow().isoformat() + 'Z',
        'stage': 'OPT1',
        'optimization_level': OPTIMIZATION_LEVEL,
        'optimization_name': 'Temporal Partitioning (geometrias)',
        'batch_id': BATCH_ID,
        'metrics': metrics_data,
        'deltas_vs_baseline': deltas
    }
    
    try:
        with open(METRICS_OUTPUT, 'w') as f:
            json.dump(output, f, indent=2)
        logger.info(f"OPT1 metrics saved to {METRICS_OUTPUT}")
    except Exception as e:
        logger.error(f"Failed to save metrics: {str(e)}")

# ============================================================================
# Main Execution
# ============================================================================

def main():
    """Main execution function"""
    logger.info("\n" + "=" * 80)
    logger.info("STAGE 4 DIA 2: OPT1 METRICS COLLECTION")
    logger.info("Optimization: Temporal Partitioning (geometrias)")
    logger.info(f"Start Time: {datetime.utcnow().isoformat()}Z")
    logger.info(f"Batch ID: {BATCH_ID}")
    logger.info(f"Optimization Level: {OPTIMIZATION_LEVEL}")
    logger.info("=" * 80)
    
    try:
        # Load baseline for comparison
        logger.info("\nLoading baseline metrics for comparison...")
        baseline_metrics = load_baseline_metrics()
        if baseline_metrics:
            logger.info("âœ“ Baseline metrics loaded")
        else:
            logger.warning("âš  No baseline metrics found - skipping delta calculations")
        
        # Connect to database
        logger.info("\nConnecting to database...")
        conn = connect_db()
        
        # Collect all metrics
        logger.info("\nCollecting OPT1 metrics...")
        metrics_data = {
            'query_latency': collect_query_latency(conn),
            'throughput': collect_throughput(conn),
            'cpu_memory_stats': collect_cpu_memory_stats(conn),
            'io_stats': collect_io_stats(conn),
            'connections': collect_connection_count(conn)
        }
        
        # Calculate deltas
        deltas = calculate_deltas(baseline_metrics, {'metrics': metrics_data})
        
        # Save to JSON
        save_metrics_to_json(metrics_data, deltas)
        
        # Close connection
        conn.close()
        
        logger.info("\n" + "=" * 80)
        logger.info("OPT1 METRICS COLLECTION COMPLETED SUCCESSFULLY")
        logger.info(f"End Time: {datetime.utcnow().isoformat()}Z")
        logger.info("=" * 80)
        
        # Print summary
        logger.info("\n" + "=" * 80)
        logger.info("OPT1 vs BASELINE SUMMARY")
        logger.info("=" * 80)
        
        if deltas.get('query_latency_deltas'):
            for query_id, delta in deltas['query_latency_deltas'].items():
                improvement = delta['improvement_percent']
                status = "âœ“ IMPROVED" if improvement > 0 else "âœ— REGRESSED"
                logger.info(f"{query_id}: {improvement:+.1f}% {status}")
        
    except Exception as e:
        logger.error(f"\nFATAL ERROR: {str(e)}")
        raise

if __name__ == '__main__':
    main()




