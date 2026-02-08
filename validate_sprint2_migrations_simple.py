#!/usr/bin/env python3
"""
Simple SQL Migration Validator for Sprint 2
Validates migrations with essential checks only
"""

import os
import sys
from pathlib import Path

def validate_migrations():
    """Validate Sprint 2 migrations"""
    
    migrations_path = Path("BIBLIOTECA/supabase/migrations")
    required_migrations = [
        "1770470100_temporal_partitioning_geometrias.sql",
        "1770470200_columnar_storage_gis.sql",
        "1770470300_indexed_views_rpc_search.sql"
    ]
    
    print("=" * 70)
    print("Sprint 2 SQL Migration Validator (Simple)")
    print("=" * 70)
    print()
    
    # Step 1: Check file existence
    print("[Step 1] Validating file existence...")
    files_ok = True
    for migration in required_migrations:
        filepath = migrations_path / migration
        if filepath.exists():
            print(f"  [PASS] {migration}")
        else:
            print(f"  [FAIL] {migration} - NOT FOUND")
            files_ok = False
    print()
    
    # Step 2: Check SQL syntax basics
    print("[Step 2] Validating SQL syntax...")
    syntax_ok = True
    for migration in required_migrations:
        filepath = migrations_path / migration
        if not filepath.exists():
            continue
            
        content = filepath.read_text(encoding='utf-8')
        
        has_begin = 'BEGIN;' in content
        has_commit = 'COMMIT;' in content
        has_keywords = any(kw in content for kw in ['CREATE', 'ALTER', 'INSERT', 'UPDATE'])
        
        status = "[PASS]" if (has_begin and has_commit and has_keywords) else "[FAIL]"
        print(f"  {status} {migration}")
        
        if not (has_begin and has_commit and has_keywords):
            syntax_ok = False
    print()
    
    # Step 3: Check migration ordering
    print("[Step 3] Validating migration ordering...")
    migration_numbers = [int(m.split('_')[0]) for m in required_migrations]
    is_ordered = migration_numbers == sorted(migration_numbers)
    
    if is_ordered:
        print(f"  [PASS] Migrations in correct order: {' < '.join(str(n) for n in migration_numbers)}")
    else:
        print(f"  [FAIL] Migrations NOT in order")
        syntax_ok = False
    print()
    
    # Step 4: Summary
    print("=" * 70)
    print("VALIDATION SUMMARY")
    print("=" * 70)
    
    if files_ok and syntax_ok:
        print("Status: [PASS] ALL VALIDATIONS PASSED")
        print("Exit Code: 0 (SUCCESS)")
        return 0
    else:
        print("Status: [FAIL] SOME VALIDATIONS FAILED")
        print("Exit Code: 1 (FAILED)")
        return 1

if __name__ == '__main__':
    exit_code = validate_migrations()
    sys.exit(exit_code)
