#!/usr/bin/env python3
"""
STAGE 4 DIA 1: Setup Benchmarking Schema
Date: FEB 7, 2026
Purpose: Create benchmarking infrastructure in PostgreSQL
"""

import psycopg2
import os
from datetime import datetime

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

LOG_FILE = 'BENCHMARKING_SETUP_LOG.txt'

def log_message(message):
    """Log message to both console and file"""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_line = f"[{timestamp}] {message}"
    print(log_line)
    with open(LOG_FILE, 'a') as f:
        f.write(log_line + '\n')

def read_sql_file(filename):
    """Read SQL file"""
    try:
        with open(filename, 'r') as f:
            return f.read()
    except Exception as e:
        log_message(f"ERROR: Failed to read {filename}: {str(e)}")
        raise

def execute_sql(conn, sql_script):
    """Execute SQL script"""
    try:
        cursor = conn.cursor()
        cursor.execute(sql_script)
        conn.commit()
        cursor.close()
        return True
    except Exception as e:
        conn.rollback()
        log_message(f"ERROR: SQL execution failed: {str(e)}")
        return False

def verify_schema(conn):
    """Verify benchmarking schema was created"""
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT COUNT(*) as table_count
            FROM information_schema.tables 
            WHERE table_schema = 'benchmarking'
        """)
        result = cursor.fetchone()
        count = result[0] if result else 0
        cursor.close()
        return count
    except Exception as e:
        log_message(f"ERROR: Schema verification failed: {str(e)}")
        return 0

def main():
    """Main execution"""
    log_message("=" * 80)
    log_message("STAGE 4 DIA 1: BENCHMARKING SCHEMA SETUP")
    log_message(f"Start Time: {datetime.now().isoformat()}")
    log_message("=" * 80)
    
    try:
        # Connect to database
        log_message(f"Connecting to PostgreSQL: {DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}")
        conn = psycopg2.connect(**DB_CONFIG)
        log_message("✓ Connected successfully")
        
        # Read SQL setup script
        log_message("Reading SQL setup script...")
        sql_script = read_sql_file('setup_benchmarking_schema.sql')
        log_message(f"✓ Script loaded ({len(sql_script)} bytes)")
        
        # Execute setup script
        log_message("Executing benchmarking schema setup...")
        if execute_sql(conn, sql_script):
            log_message("✓ Schema setup completed successfully")
        else:
            raise Exception("Failed to execute SQL setup script")
        
        # Verify schema
        log_message("Verifying schema creation...")
        table_count = verify_schema(conn)
        log_message(f"✓ Benchmarking schema verified ({table_count} tables created)")
        
        # Close connection
        conn.close()
        
        log_message("=" * 80)
        log_message("SETUP COMPLETED SUCCESSFULLY")
        log_message(f"End Time: {datetime.now().isoformat()}")
        log_message("=" * 80)
        
    except Exception as e:
        log_message(f"FATAL ERROR: {str(e)}")
        raise

if __name__ == '__main__':
    main()
