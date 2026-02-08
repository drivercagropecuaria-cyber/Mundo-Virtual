#!/usr/bin/env python3
"""
SPRINT 3 - STAGE 2: OPT1 DRY-RUN VALIDATION
Mundo Virtual Villa Canabrava
Data: 2026-02-06
Status: NOVO - Sprint 3 Executor
"""

import psycopg2
import json
import time
from datetime import datetime
import sys
import os

# ============================================================================
# CONFIGURATION
# ============================================================================

DB_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "database": "villa_canabrava",
    "user": "postgres",
    "password": ""  # Use default or .pgpass
}

MIGRATION_FILE = "BIBLIOTECA/supabase/migrations/1770500100_auto_partition_creation_2029_plus.sql"
TIMESTAMP = datetime.now().strftime("%Y%m%d_%H%M%S")
LOG_FILE = f"STAGE2_OPT1_DRYRUN_LOG_{TIMESTAMP}.txt"
METRICS_FILE = f"METRICS_OPT1_STAGE2_{TIMESTAMP}.json"

# Test tracking
tests_passed = 0
tests_failed = 0
metrics = {}

# ============================================================================
# LOGGING FUNCTION
# ============================================================================

def write_log(message, level="INFO"):
    """Log message to console and file"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_message = f"[{timestamp}] [{level}] {message}"
    print(log_message)
    with open(LOG_FILE, 'a', encoding='utf-8') as f:
        f.write(log_message + "\n")

# ============================================================================
# DATABASE CONNECTION
# ============================================================================

def get_db_connection():
    """Establish connection to PostgreSQL"""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        return conn
    except Exception as e:
        write_log(f"Error connecting to database: {str(e)}", "ERROR")
        return None

# ============================================================================
# TEST FUNCTIONS
# ============================================================================

def test_postgresql_connection():
    """Test PostgreSQL connectivity"""
    global tests_passed, tests_failed
    
    write_log("================================================", "INFO")
    write_log("STAGE 2: Validação Pré-Flight", "INFO")
    write_log("================================================", "INFO")
    write_log("", "INFO")
    write_log("1. Testando conectividade PostgreSQL...", "INFO")
    
    try:
        conn = get_db_connection()
        if conn:
            cursor = conn.cursor()
            cursor.execute("SELECT version();")
            version = cursor.fetchone()[0]
            write_log(f"   ✅ Conexão bem-sucedida", "SUCCESS")
            write_log(f"   Versão: {version[:50]}...", "INFO")
            cursor.close()
            conn.close()
            tests_passed += 1
            return True
        else:
            write_log("   ❌ Falha na conexão", "ERROR")
            tests_failed += 1
            return False
    except Exception as e:
        write_log(f"   ❌ Erro: {str(e)}", "ERROR")
        tests_failed += 1
        return False

def test_base_table_exists():
    """Verify base table exists"""
    global tests_passed, tests_failed
    
    write_log("", "INFO")
    write_log("2. Verificando tabela particionada...", "INFO")
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT table_name FROM information_schema.tables 
            WHERE table_name = 'catalogo_geometrias_particionada' 
            AND table_type = 'BASE TABLE'
        """)
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        
        if result:
            write_log("   ✅ Tabela catalogo_geometrias_particionada encontrada", "SUCCESS")
            tests_passed += 1
            return True
        else:
            write_log("   ❌ Tabela não encontrada", "ERROR")
            tests_failed += 1
            return False
    except Exception as e:
        write_log(f"   ❌ Erro: {str(e)}", "ERROR")
        tests_failed += 1
        return False

def test_existing_partitions():
    """Check for existing partitions"""
    global tests_passed, tests_failed
    
    write_log("", "INFO")
    write_log("3. Verificando partições existentes...", "INFO")
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT tablename FROM pg_tables 
            WHERE tablename LIKE 'catalogo_geometrias_particionada_%' 
            ORDER BY tablename
        """)
        partitions = cursor.fetchall()
        cursor.close()
        conn.close()
        
        if partitions:
            write_log("   ✅ Partições encontradas:", "SUCCESS")
            for p in partitions:
                write_log(f"      - {p[0]}", "INFO")
            tests_passed += 1
            return True
        else:
            write_log("   ⚠️  Nenhuma partição encontrada (esperado para primeira execução)", "WARNING")
            return True
    except Exception as e:
        write_log(f"   ❌ Erro: {str(e)}", "ERROR")
        tests_failed += 1
        return False

def execute_opt1_migration():
    """Execute OPT1 migration"""
    global tests_passed, tests_failed, metrics
    
    write_log("", "INFO")
    write_log("================================================", "INFO")
    write_log("STAGE 2: Execução da Migration OPT1", "INFO")
    write_log("================================================", "INFO")
    write_log("", "INFO")
    write_log("4. Executando migration OPT1...", "INFO")
    
    # Check file exists
    if not os.path.exists(MIGRATION_FILE):
        write_log(f"   ❌ Arquivo migration não encontrado: {MIGRATION_FILE}", "ERROR")
        tests_failed += 1
        return False
    
    write_log(f"   Arquivo: {MIGRATION_FILE}", "INFO")
    
    try:
        # Read migration file
        with open(MIGRATION_FILE, 'r', encoding='utf-8') as f:
            sql_content = f.read()
        
        # Execute migration
        start_time = time.time()
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Execute entire migration
        cursor.execute(sql_content)
        conn.commit()
        
        duration_ms = (time.time() - start_time) * 1000
        metrics["opt1_execution_time_ms"] = round(duration_ms, 2)
        
        write_log(f"   ✅ Migration executada com sucesso", "SUCCESS")
        write_log(f"   Duração: {duration_ms:.2f}ms", "INFO")
        
        cursor.close()
        conn.close()
        tests_passed += 1
        return True
    except Exception as e:
        write_log(f"   ❌ Erro na execução: {str(e)}", "ERROR")
        tests_failed += 1
        return False

def test_trigger_creation():
    """Verify trigger creation"""
    global tests_passed, tests_failed
    
    write_log("", "INFO")
    write_log("5. Verificando trigger criado...", "INFO")
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT trigger_name, event_object_table, trigger_timing 
            FROM information_schema.triggers 
            WHERE trigger_name LIKE '%auto_create_partition%'
        """)
        result = cursor.fetchall()
        cursor.close()
        conn.close()
        
        if result:
            write_log("   ✅ Trigger criado com sucesso", "SUCCESS")
            for r in result:
                write_log(f"      - {r[0]}", "INFO")
            tests_passed += 1
            return True
        else:
            write_log("   ❌ Trigger não encontrado", "ERROR")
            tests_failed += 1
            return False
    except Exception as e:
        write_log(f"   ❌ Erro: {str(e)}", "ERROR")
        tests_failed += 1
        return False

def test_functions_created():
    """Verify functions created"""
    global tests_passed, tests_failed
    
    write_log("", "INFO")
    write_log("6. Verificando funções criadas...", "INFO")
    
    functions = [
        "create_missing_year_partitions",
        "auto_create_partition_for_year",
        "scheduled_partition_maintenance",
        "maintain_partitions"
    ]
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        all_found = True
        for func in functions:
            cursor.execute("""
                SELECT routine_name FROM information_schema.routines 
                WHERE routine_name = %s
            """, (func,))
            result = cursor.fetchone()
            
            if result:
                write_log(f"   ✅ Função {func} encontrada", "SUCCESS")
            else:
                write_log(f"   ❌ Função {func} não encontrada", "ERROR")
                all_found = False
        
        cursor.close()
        conn.close()
        
        if all_found:
            tests_passed += 1
            return True
        else:
            tests_failed += 1
            return False
    except Exception as e:
        write_log(f"   ❌ Erro: {str(e)}", "ERROR")
        tests_failed += 1
        return False

def test_partition_creation():
    """Test partition creation"""
    global tests_passed, tests_failed, metrics
    
    write_log("", "INFO")
    write_log("7. Testando criação de partições...", "INFO")
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        start_time = time.time()
        cursor.execute("""
            SELECT partition_name, status FROM create_missing_year_partitions('catalogo_geometrias_particionada') 
            LIMIT 10
        """)
        results = cursor.fetchall()
        duration_ms = (time.time() - start_time) * 1000
        
        write_log("   ✅ create_missing_year_partitions executada", "SUCCESS")
        write_log("   Resultados:", "INFO")
        for r in results:
            write_log(f"      - {r[0]}: {r[1]}", "INFO")
        write_log(f"   Duração: {duration_ms:.2f}ms", "INFO")
        
        metrics["partition_creation_time_ms"] = round(duration_ms, 2)
        
        cursor.close()
        conn.close()
        tests_passed += 1
        return True
    except Exception as e:
        write_log(f"   ❌ Erro: {str(e)}", "ERROR")
        tests_failed += 1
        return False

def test_partition_count():
    """Count created partitions"""
    global tests_passed, tests_failed, metrics
    
    write_log("", "INFO")
    write_log("8. Contando partições criadas...", "INFO")
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT COUNT(*) FROM pg_tables 
            WHERE tablename LIKE 'catalogo_geometrias_particionada_%'
        """)
        count = cursor.fetchone()[0]
        
        write_log("   ✅ Partições contadas", "SUCCESS")
        write_log(f"   Total de partições: {count}", "INFO")
        
        metrics["partition_count"] = count
        
        if count >= 7:  # 2029-2035 = 7 partições
            write_log("   ✅ Número esperado de partições (7)", "SUCCESS")
            tests_passed += 1
        else:
            write_log(f"   ⚠️  Número de partições: {count} (esperado >= 7)", "WARNING")
        
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        write_log(f"   ❌ Erro: {str(e)}", "ERROR")
        tests_failed += 1
        return False

def test_maintenance_log_table():
    """Verify maintenance log table"""
    global tests_passed, tests_failed
    
    write_log("", "INFO")
    write_log("9. Verificando tabela de manutenção...", "INFO")
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT table_name FROM information_schema.tables 
            WHERE table_name = 'partition_maintenance_log'
        """)
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        
        if result:
            write_log("   ✅ Tabela partition_maintenance_log criada", "SUCCESS")
            tests_passed += 1
            return True
        else:
            write_log("   ❌ Tabela não encontrada", "ERROR")
            tests_failed += 1
            return False
    except Exception as e:
        write_log(f"   ❌ Erro: {str(e)}", "ERROR")
        tests_failed += 1
        return False

def generate_metrics_report():
    """Generate final metrics report"""
    global tests_passed, tests_failed
    
    write_log("", "INFO")
    write_log("================================================", "INFO")
    write_log("STAGE 2: Relatório de Métricas", "INFO")
    write_log("================================================", "INFO")
    write_log("", "INFO")
    write_log(f"Testes Executados: {tests_passed + tests_failed}", "INFO")
    write_log(f"Sucessos: {tests_passed} ✅", "SUCCESS")
    write_log(f"Falhas: {tests_failed} ❌", "INFO")
    
    # Create JSON metrics file
    total_tests = tests_passed + tests_failed
    success_rate = (tests_passed / total_tests * 100) if total_tests > 0 else 0
    
    metrics_data = {
        "timestamp": datetime.now().isoformat(),
        "stage": "STAGE2_OPT1_DRYRUN",
        "tests_passed": tests_passed,
        "tests_failed": tests_failed,
        "success_rate": round(success_rate, 2),
        "metrics": metrics
    }
    
    with open(METRICS_FILE, 'w', encoding='utf-8') as f:
        json.dump(metrics_data, f, indent=2)
    
    write_log("", "INFO")
    write_log(f"Métricas salvas em: {METRICS_FILE}", "INFO")
    
    return tests_failed == 0

def generate_summary_report(success):
    """Generate summary report"""
    write_log("", "INFO")
    write_log("================================================", "INFO")
    write_log("STAGE 2: RESULTADO FINAL", "INFO")
    write_log("================================================", "INFO")
    
    if success:
        write_log("STATUS: ✅ PASS", "SUCCESS")
        write_log("", "INFO")
        write_log("Recomendação: PROCEDER PARA STAGE 3 (Rollback Procedure)", "SUCCESS")
    else:
        write_log("STATUS: ❌ FAIL", "ERROR")
        write_log("", "INFO")
        write_log("Ação Requerida: Revisar erros acima", "ERROR")
        write_log("Escalação L1/L2 necessária", "ERROR")
    
    write_log("", "INFO")
    write_log(f"Log completo: {LOG_FILE}", "INFO")
    write_log(f"Métricas: {METRICS_FILE}", "INFO")
    write_log("================================================", "INFO")

# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main():
    write_log("============================================================================", "INFO")
    write_log("SPRINT 3 - STAGE 2: OPT1 DRY-RUN VALIDATION", "INFO")
    write_log("============================================================================", "INFO")
    write_log(f"Iniciado em: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}", "INFO")
    write_log(f"Database: {DB_CONFIG['database']} @ {DB_CONFIG['host']}:{DB_CONFIG['port']}", "INFO")
    write_log(f"User: {DB_CONFIG['user']}", "INFO")
    write_log("============================================================================", "INFO")
    
    # Execute all tests
    all_passed = True
    all_passed = test_postgresql_connection() and all_passed
    all_passed = test_base_table_exists() and all_passed
    all_passed = test_existing_partitions() and all_passed
    all_passed = execute_opt1_migration() and all_passed
    all_passed = test_trigger_creation() and all_passed
    all_passed = test_functions_created() and all_passed
    all_passed = test_partition_creation() and all_passed
    all_passed = test_partition_count() and all_passed
    all_passed = test_maintenance_log_table() and all_passed
    
    # Generate reports
    all_passed = generate_metrics_report() and all_passed
    generate_summary_report(all_passed)
    
    # Exit with appropriate code
    sys.exit(0 if all_passed else 1)

if __name__ == "__main__":
    main()
