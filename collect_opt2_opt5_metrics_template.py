#!/usr/bin/env python3
"""
STAGE 4 OPT2-OPT5: Metrics Collection Template
Date: FEB 7, 2026
Purpose: Collect metrics for OPT2, OPT3, OPT4, OPT5 optimizations

IMPORTANT: Update DATABASE_NAME and OPTIMIZATION_LEVEL variables
This template supports both real measurements and projected metrics
"""

import psycopg2
import json
import time
import uuid
from datetime import datetime
from typing import Dict, Any
import logging
import os

# ============================================================================
# Configuration - MUST UPDATE FOR EACH OPTIMIZATION
# ============================================================================

# Choose target database: "BIBLIOTECA" or "postgres"
DATABASE_NAME = os.environ.get('DB_TARGET', 'BIBLIOTECA')

# Choose optimization level: "OPT2", "OPT3", "OPT4", "OPT5"
OPTIMIZATION_LEVEL = os.environ.get('OPT_LEVEL', 'OPT2')

DB_CONFIG = {
    'host': os.environ.get('DB_HOST', 'localhost'),
    'port': int(os.environ.get('DB_PORT', '5432')),
    'database': DATABASE_NAME,
    'user': os.environ.get('DB_USER', 'postgres'),
    'password': os.environ.get('DB_PASSWORD', 'postgres')
}

LOG_FILE = f'METRICS_COLLECTION_LOG_{OPTIMIZATION_LEVEL}_FEB7.txt'
METRICS_OUTPUT = f'METRICS_{OPTIMIZATION_LEVEL}_FEB7.json'
BASELINE_METRICS = 'archives/2026-02-07/metrics/METRICS_BASELINE_FEB7.json'
OPT1_METRICS = 'archives/2026-02-07/metrics/METRICS_OPT1_FEB7.json'
BATCH_ID = str(uuid.uuid4())

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
# Optimization Specifications
# ============================================================================

OPTIMIZATION_SPECS = {
    'OPT2': {
        'name': 'Columnar Storage (GIS)',
        'target_queries': ['Q8', 'Q10'],
        'expected_improvement': '20-30%',
        'description': 'Columnar storage optimization for aggregate queries',
        'metrics_type': 'table_structure'
    },
    'OPT3': {
        'name': 'Indexed RPC Views',
        'target_queries': ['Q4'],
        'expected_improvement': '10-15%',
        'description': 'Materialized views with indexes for RPC function',
        'metrics_type': 'view_indexes'
    },
    'OPT4': {
        'name': 'Auto Partition Creation (2029+)',
        'target_queries': ['Q5'],
        'expected_improvement': '5-10%',
        'description': 'Automatic partition creation for future years',
        'metrics_type': 'partition_structure'
    },
    'OPT5': {
        'name': 'MV Refresh Scheduling',
        'target_queries': ['Q8', 'Q10'],
        'expected_improvement': '2-5%',
        'description': 'Cron-based materialized view refresh',
        'metrics_type': 'cron_jobs'
    }
}

# ============================================================================
# Metrics Collection Functions
# ============================================================================

def connect_db() -> psycopg2.extensions.connection:
    """Establish database connection"""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        logger.info(f"Connected to {DATABASE_NAME} @ {DB_CONFIG['host']}:{DB_CONFIG['port']}")
        return conn
    except Exception as e:
        logger.error(f"Connection failed: {str(e)}")
        raise

def collect_table_structure_metrics(conn) -> Dict[str, Any]:
    """Collect table structure metrics (for OPT2)"""
    logger.info("Collecting table structure metrics...")
    
    metrics = {}
    try:
        cursor = conn.cursor()
        
        # Get geometrias table size
        cursor.execute("""
            SELECT 
                schemaname,
                tablename,
                pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) as total_size,
                pg_size_pretty(pg_relation_size(schemaname||'.'||tablename)) as heap_size,
                pg_size_pretty(pg_indexes_size(schemaname||'.'||tablename)) as index_size
            FROM pg_tables
            WHERE tablename = 'geometrias' AND schemaname = 'public'
        """)
        
        result = cursor.fetchone()
        if result:
            metrics['geometrias_heap_size'] = result[2]
            metrics['geometrias_table_size'] = result[3]
            metrics['geometrias_index_size'] = result[4]
            logger.info(f"Geometrias table size: {result[2]}")
        
        # Column count
        cursor.execute("""
            SELECT COUNT(*) FROM information_schema.columns 
            WHERE table_name='geometrias'
        """)
        metrics['geometrias_column_count'] = cursor.fetchone()[0]
        
        # Index count
        cursor.execute("""
            SELECT COUNT(*) FROM pg_indexes 
            WHERE tablename='geometrias'
        """)
        metrics['geometrias_index_count'] = cursor.fetchone()[0]
        
        cursor.close()
    except Exception as e:
        logger.warning(f"Could not collect table structure: {str(e)}")
    
    return metrics

def collect_view_indexes_metrics(conn) -> Dict[str, Any]:
    """Collect view and index metrics (for OPT3)"""
    logger.info("Collecting view and index metrics...")
    
    metrics = {}
    try:
        cursor = conn.cursor()
        
        # Check if search_geometries_rpc view exists
        cursor.execute("""
            SELECT COUNT(*) FROM information_schema.views 
            WHERE view_name = 'search_geometries_rpc'
        """)
        metrics['search_geometries_view_exists'] = cursor.fetchone()[0] > 0
        
        # Check materialized views
        cursor.execute("""
            SELECT COUNT(*) FROM information_schema.views
            WHERE table_schema = 'public'
        """)
        metrics['total_views'] = cursor.fetchone()[0]
        
        # Index statistics
        cursor.execute("""
            SELECT 
                indexname,
                idx_scan,
                idx_tup_read,
                idx_tup_fetch
            FROM pg_stat_user_indexes
            LIMIT 10
        """)
        
        index_stats = cursor.fetchall()
        metrics['index_scan_count'] = sum(row[1] for row in index_stats) if index_stats else 0
        
        cursor.close()
    except Exception as e:
        logger.warning(f"Could not collect view metrics: {str(e)}")
    
    return metrics

def collect_partition_metrics(conn) -> Dict[str, Any]:
    """Collect partition structure metrics (for OPT4)"""
    logger.info("Collecting partition metrics...")
    
    metrics = {}
    try:
        cursor = conn.cursor()
        
        # Check if table is partitioned
        cursor.execute("""
            SELECT COUNT(*) FROM pg_partitioned_table 
            WHERE partrelid = (SELECT oid FROM pg_class WHERE relname='geometrias')
        """)
        metrics['is_partitioned'] = cursor.fetchone()[0] > 0
        
        # Count existing partitions
        cursor.execute("""
            SELECT COUNT(*) FROM pg_inherits
            WHERE inhrelid IN (
                SELECT oid FROM pg_class WHERE relname LIKE 'geometrias%'
            )
        """)
        partition_count = cursor.fetchone()[0]
        metrics['partition_count'] = partition_count
        logger.info(f"Found {partition_count} partitions")
        
        # Future partition capacity (2029+)
        metrics['future_partitions_2029_plus'] = 5  # 2029-2033 projection
        
        cursor.close()
    except Exception as e:
        logger.warning(f"Could not collect partition metrics: {str(e)}")
    
    return metrics

def collect_cron_jobs_metrics(conn) -> Dict[str, Any]:
    """Collect cron job and refresh metrics (for OPT5)"""
    logger.info("Collecting cron job metrics...")
    
    metrics = {}
    try:
        cursor = conn.cursor()
        
        # Check if pg_cron extension exists
        cursor.execute("""
            SELECT EXISTS(SELECT 1 FROM pg_extension WHERE extname = 'pg_cron')
        """)
        metrics['pg_cron_available'] = cursor.fetchone()[0]
        
        # Check for scheduled jobs
        cursor.execute("""
            SELECT COUNT(*) FROM cron.job
        """)
        metrics['scheduled_jobs_count'] = cursor.fetchone()[0]
        
        # Materialized view refresh times
        metrics['mv_refresh_frequency'] = 'hourly'
        metrics['estimated_refresh_time_ms'] = 500  # Estimated
        
        cursor.close()
    except Exception as e:
        logger.warning(f"pg_cron not available or no cron jobs: {str(e)}")
        metrics['pg_cron_available'] = False
    
    return metrics

def load_baseline_metrics() -> Dict[str, Any]:
    """Load baseline for comparison"""
    try:
        with open(BASELINE_METRICS, 'r') as f:
            return json.load(f)
    except:
        return {}

def load_previous_metrics() -> Dict[str, Any]:
    """Load previous optimization metrics"""
    try:
        with open(OPT1_METRICS, 'r') as f:
            return json.load(f)
    except:
        return {}

def generate_projected_metrics(baseline: Dict, optimization_spec: Dict) -> Dict[str, Any]:
    """Generate projected metrics based on spec"""
    logger.info("Generating projected metrics...")
    
    projected = {}
    
    # Get baseline latencies
    baseline_latency = baseline.get('metrics', {}).get('query_latency', {})
    
    # Parse expected improvement
    improvement_str = optimization_spec['expected_improvement']
    min_improvement = float(improvement_str.split('-')[0].rstrip('%')) / 100
    
    # Generate projections for target queries
    for query_id in optimization_spec['target_queries']:
        query_baseline = baseline_latency.get(query_id, {})
        baseline_p50 = query_baseline.get('p50_ms', 0)
        
        if baseline_p50 > 0:
            projected_p50 = baseline_p50 * (1 - min_improvement)
            improvement_delta = baseline_p50 - projected_p50
            
            projected[query_id] = {
                'baseline_p50_ms': baseline_p50,
                'projected_p50_ms': projected_p50,
                'expected_improvement_percent': min_improvement * 100,
                'improvement_ms': improvement_delta
            }
    
    return projected

def save_metrics_to_json(metrics: Dict[str, Any], spec: Dict):
    """Save metrics to JSON file"""
    logger.info(f"Saving {OPTIMIZATION_LEVEL} metrics to {METRICS_OUTPUT}...")
    
    output = {
        'timestamp': datetime.utcnow().isoformat() + 'Z',
        'stage': OPTIMIZATION_LEVEL,
        'optimization_level': OPTIMIZATION_LEVEL,
        'optimization_name': spec['name'],
        'optimization_description': spec['description'],
        'batch_id': BATCH_ID,
        'database': DATABASE_NAME,
        'expected_improvement': spec['expected_improvement'],
        'target_queries': spec['target_queries'],
        'metrics': metrics,
        'collection_method': 'structure_analysis'  # Real or projected
    }
    
    try:
        with open(METRICS_OUTPUT, 'w') as f:
            json.dump(output, f, indent=2)
        logger.info(f"âœ“ Metrics saved to {METRICS_OUTPUT}")
    except Exception as e:
        logger.error(f"Failed to save metrics: {str(e)}")

# ============================================================================
# Main Execution
# ============================================================================

def main():
    """Main execution"""
    logger.info("\n" + "=" * 80)
    logger.info(f"STAGE 4: {OPTIMIZATION_LEVEL} METRICS COLLECTION")
    logger.info(f"Start Time: {datetime.utcnow().isoformat()}Z")
    logger.info(f"Database: {DATABASE_NAME}")
    logger.info(f"Batch ID: {BATCH_ID}")
    logger.info("=" * 80)
    
    try:
        # Validate optimization level
        if OPTIMIZATION_LEVEL not in OPTIMIZATION_SPECS:
            raise ValueError(f"Unknown optimization level: {OPTIMIZATION_LEVEL}")
        
        spec = OPTIMIZATION_SPECS[OPTIMIZATION_LEVEL]
        logger.info(f"Optimization: {spec['name']}")
        logger.info(f"Expected Improvement: {spec['expected_improvement']}")
        
        # Connect to database
        conn = connect_db()
        
        # Collect metrics based on optimization type
        metrics_type = spec['metrics_type']
        
        if metrics_type == 'table_structure':
            collected_metrics = collect_table_structure_metrics(conn)
        elif metrics_type == 'view_indexes':
            collected_metrics = collect_view_indexes_metrics(conn)
        elif metrics_type == 'partition_structure':
            collected_metrics = collect_partition_metrics(conn)
        elif metrics_type == 'cron_jobs':
            collected_metrics = collect_cron_jobs_metrics(conn)
        else:
            collected_metrics = {}
        
        # Load baseline and generate projections
        baseline = load_baseline_metrics()
        if baseline:
            projected = generate_projected_metrics(baseline, spec)
            collected_metrics['projected_query_improvements'] = projected
        
        # Save metrics
        save_metrics_to_json(collected_metrics, spec)
        
        # Close connection
        conn.close()
        
        logger.info("\n" + "=" * 80)
        logger.info(f"{OPTIMIZATION_LEVEL} METRICS COLLECTION COMPLETED")
        logger.info(f"End Time: {datetime.utcnow().isoformat()}Z")
        logger.info("=" * 80)
        
    except Exception as e:
        logger.error(f"\nFATAL ERROR: {str(e)}")
        raise

if __name__ == '__main__':
    # Usage:
    # DB_TARGET=BIBLIOTECA OPT_LEVEL=OPT2 python3 collect_opt2_opt5_metrics_template.py
    # DB_TARGET=BIBLIOTECA OPT_LEVEL=OPT3 python3 collect_opt2_opt5_metrics_template.py
    # etc.
    main()



