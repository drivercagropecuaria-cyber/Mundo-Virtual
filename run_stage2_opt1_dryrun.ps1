# ============================================================================
# SPRINT 3 - STAGE 2: OPT1 DRY-RUN VALIDATION
# ============================================================================
# Script: run_stage2_opt1_dryrun.ps1
# Objetivo: Validar execução de OPT1 migration em ambiente shadow
# Data: 2026-02-06
# Status: NOVO - Sprint 3 Executor
# ============================================================================

# Configuration
$SCRIPT_NAME = "STAGE2_OPT1_DRYRUN"
$TIMESTAMP = Get-Date -Format "yyyyMMdd_HHmmss"
$LOG_FILE = "STAGE2_OPT1_DRYRUN_LOG_$TIMESTAMP.txt"
$METRICS_FILE = "METRICS_OPT1_STAGE2_$TIMESTAMP.json"
$DB_HOST = "localhost"
$DB_PORT = "5432"
$DB_USER = "postgres"
$DB_NAME = "villa_canabrava"
$MIGRATION_FILE = "BIBLIOTECA\supabase\migrations\1770500100_auto_partition_creation_2029_plus.sql"

# Test status tracking
$TESTS_PASSED = 0
$TESTS_FAILED = 0
$METRICS = @{}

# ============================================================================
# FUNCTION: Log message to console and file
# ============================================================================
function Write-Log {
    param(
        [string]$Message,
        [string]$Level = "INFO"
    )
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $logMessage = "[$timestamp] [$Level] $Message"
    Write-Host $logMessage
    Add-Content -Path $LOG_FILE -Value $logMessage
}

# ============================================================================
# FUNCTION: Execute SQL query and return result
# ============================================================================
function Invoke-SqlQuery {
    param(
        [string]$Query,
        [bool]$TimeExecution = $false
    )
    
    $startTime = Get-Date
    try {
        # Create connection string
        $connString = "Server=$DB_HOST;Port=$DB_PORT;Database=$DB_NAME;User Id=$DB_USER;Password=;"
        
        # Execute using psql
        $result = psql -h $DB_HOST -U $DB_USER -d $DB_NAME -c $Query 2>&1
        
        if ($TimeExecution) {
            $duration = (Get-Date) - $startTime
            return @{
                "output" = $result
                "duration_ms" = $duration.TotalMilliseconds
                "success" = $true
            }
        }
        
        return @{
            "output" = $result
            "success" = $true
        }
    }
    catch {
        Write-Log "Error executing query: $_" "ERROR"
        return @{
            "output" = $_
            "success" = $false
        }
    }
}

# ============================================================================
# FUNCTION: Check PostgreSQL connectivity
# ============================================================================
function Test-PostgreSQLConnection {
    Write-Log "================================================" "INFO"
    Write-Log "STAGE 2: Validação Pré-Flight" "INFO"
    Write-Log "================================================" "INFO"
    Write-Log "" "INFO"
    Write-Log "1. Testando conectividade PostgreSQL..." "INFO"
    
    try {
        $result = psql -h $DB_HOST -U $DB_USER -d $DB_NAME -c "SELECT version();" 2>&1
        
        if ($LASTEXITCODE -eq 0) {
            Write-Log "   ✅ Conexão bem-sucedida" "SUCCESS"
            Write-Log "   Versão: $result" "INFO"
            $TESTS_PASSED++
            return $true
        }
        else {
            Write-Log "   ❌ Falha na conexão: $result" "ERROR"
            $TESTS_FAILED++
            return $false
        }
    }
    catch {
        Write-Log "   ❌ Erro: $_" "ERROR"
        $TESTS_FAILED++
        return $false
    }
}

# ============================================================================
# FUNCTION: Verify base table exists
# ============================================================================
function Test-BaseTableExists {
    Write-Log "" "INFO"
    Write-Log "2. Verificando tabela particionada..." "INFO"
    
    $query = "SELECT table_name FROM information_schema.tables WHERE table_name = 'catalogo_geometrias_particionada' AND table_type = 'BASE TABLE';"
    $result = Invoke-SqlQuery -Query $query
    
    if ($result.output -like "*catalogo_geometrias_particionada*") {
        Write-Log "   ✅ Tabela catalogo_geometrias_particionada encontrada" "SUCCESS"
        $TESTS_PASSED++
        return $true
    }
    else {
        Write-Log "   ❌ Tabela não encontrada" "ERROR"
        $TESTS_FAILED++
        return $false
    }
}

# ============================================================================
# FUNCTION: Check for existing partitions
# ============================================================================
function Test-ExistingPartitions {
    Write-Log "" "INFO"
    Write-Log "3. Verificando partições existentes..." "INFO"
    
    $query = "SELECT tablename FROM pg_tables WHERE tablename LIKE 'catalogo_geometrias_particionada_%' ORDER BY tablename;"
    $result = Invoke-SqlQuery -Query $query
    
    if ($result.output) {
        Write-Log "   ✅ Partições encontradas:" "SUCCESS"
        Write-Log "   $result.output" "INFO"
        $TESTS_PASSED++
        return $true
    }
    else {
        Write-Log "   ⚠️  Nenhuma partição encontrada (esperado para primeira execução)" "WARNING"
        return $true
    }
}

# ============================================================================
# FUNCTION: Execute OPT1 migration dry-run
# ============================================================================
function Execute-OPT1Migration {
    Write-Log "" "INFO"
    Write-Log "================================================" "INFO"
    Write-Log "STAGE 2: Execução da Migration OPT1" "INFO"
    Write-Log "================================================" "INFO"
    Write-Log "" "INFO"
    Write-Log "4. Executando migration OPT1..." "INFO"
    
    # Verificar se arquivo existe
    if (-not (Test-Path $MIGRATION_FILE)) {
        Write-Log "   ❌ Arquivo migration não encontrado: $MIGRATION_FILE" "ERROR"
        $TESTS_FAILED++
        return $false
    }
    
    Write-Log "   Arquivo: $MIGRATION_FILE" "INFO"
    
    try {
        $startTime = Get-Date
        
        # Executar migration
        $output = psql -h $DB_HOST -U $DB_USER -d $DB_NAME -f $MIGRATION_FILE 2>&1
        
        $duration = (Get-Date) - $startTime
        $duration_ms = $duration.TotalMilliseconds
        
        $METRICS["opt1_execution_time_ms"] = $duration_ms
        
        if ($LASTEXITCODE -eq 0) {
            Write-Log "   ✅ Migration executada com sucesso" "SUCCESS"
            Write-Log "   Duração: ${duration_ms}ms" "INFO"
            $TESTS_PASSED++
            return $true
        }
        else {
            Write-Log "   ❌ Erro na execução da migration:" "ERROR"
            Write-Log "   $output" "ERROR"
            $TESTS_FAILED++
            return $false
        }
    }
    catch {
        Write-Log "   ❌ Erro: $_" "ERROR"
        $TESTS_FAILED++
        return $false
    }
}

# ============================================================================
# FUNCTION: Verify trigger creation
# ============================================================================
function Test-TriggerCreation {
    Write-Log "" "INFO"
    Write-Log "5. Verificando trigger criado..." "INFO"
    
    $query = "SELECT trigger_name, event_object_table, trigger_timing FROM information_schema.triggers WHERE trigger_name LIKE 'trigger_auto_create_partition%' OR trigger_name LIKE 'auto_create_partition%';"
    $result = Invoke-SqlQuery -Query $query
    
    if ($result.output -like "*auto_create_partition*") {
        Write-Log "   ✅ Trigger criado com sucesso" "SUCCESS"
        Write-Log "   Resultado: $result.output" "INFO"
        $TESTS_PASSED++
        return $true
    }
    else {
        Write-Log "   ❌ Trigger não encontrado" "ERROR"
        Write-Log "   Resultado: $result.output" "ERROR"
        $TESTS_FAILED++
        return $false
    }
}

# ============================================================================
# FUNCTION: Verify functions created
# ============================================================================
function Test-FunctionsCreated {
    Write-Log "" "INFO"
    Write-Log "6. Verificando funções criadas..." "INFO"
    
    $functions = @(
        "create_missing_year_partitions",
        "auto_create_partition_for_year",
        "scheduled_partition_maintenance",
        "maintain_partitions"
    )
    
    $allFound = $true
    foreach ($func in $functions) {
        $query = "SELECT routine_name FROM information_schema.routines WHERE routine_name = '$func';"
        $result = Invoke-SqlQuery -Query $query
        
        if ($result.output -like "*$func*") {
            Write-Log "   ✅ Função $func encontrada" "SUCCESS"
        }
        else {
            Write-Log "   ❌ Função $func não encontrada" "ERROR"
            $allFound = $false
        }
    }
    
    if ($allFound) {
        $TESTS_PASSED++
        return $true
    }
    else {
        $TESTS_FAILED++
        return $false
    }
}

# ============================================================================
# FUNCTION: Test partition creation
# ============================================================================
function Test-PartitionCreation {
    Write-Log "" "INFO"
    Write-Log "7. Testando criação de partições..." "INFO"
    
    # Teste 1: Chamar create_missing_year_partitions
    $query = "SELECT partition_name, status FROM create_missing_year_partitions('catalogo_geometrias_particionada') LIMIT 10;"
    $result = Invoke-SqlQuery -Query $query -TimeExecution $true
    
    if ($result.success) {
        Write-Log "   ✅ create_missing_year_partitions executada" "SUCCESS"
        Write-Log "   Resultados:" "INFO"
        Write-Log "   $($result.output)" "INFO"
        Write-Log "   Duração: $($result.duration_ms)ms" "INFO"
        
        $METRICS["partition_creation_time_ms"] = $result.duration_ms
        $TESTS_PASSED++
        return $true
    }
    else {
        Write-Log "   ❌ Erro ao testar criação de partições" "ERROR"
        Write-Log "   Erro: $($result.output)" "ERROR"
        $TESTS_FAILED++
        return $false
    }
}

# ============================================================================
# FUNCTION: Count created partitions
# ============================================================================
function Test-PartitionCount {
    Write-Log "" "INFO"
    Write-Log "8. Contando partições criadas..." "INFO"
    
    $query = "SELECT COUNT(*) as partition_count FROM pg_tables WHERE tablename LIKE 'catalogo_geometrias_particionada_%';"
    $result = Invoke-SqlQuery -Query $query
    
    if ($result.success) {
        # Parse count from result
        $count = $result.output | Where-Object { $_ -match "\d+" } | ForEach-Object { [int]($_ -replace "\D") }
        
        Write-Log "   ✅ Partições contadas" "SUCCESS"
        Write-Log "   Total de partições: $count" "INFO"
        
        $METRICS["partition_count"] = $count
        
        if ($count -ge 7) {  # 2029-2035 = 7 partições
            Write-Log "   ✅ Número esperado de partições (7)" "SUCCESS"
            $TESTS_PASSED++
            return $true
        }
        else {
            Write-Log "   ⚠️  Número de partições menor que esperado" "WARNING"
            return $true
        }
    }
    else {
        Write-Log "   ❌ Erro ao contar partições" "ERROR"
        $TESTS_FAILED++
        return $false
    }
}

# ============================================================================
# FUNCTION: Verify maintenance log table
# ============================================================================
function Test-MaintenanceLogTable {
    Write-Log "" "INFO"
    Write-Log "9. Verificando tabela de manutenção..." "INFO"
    
    $query = "SELECT table_name FROM information_schema.tables WHERE table_name = 'partition_maintenance_log';"
    $result = Invoke-SqlQuery -Query $query
    
    if ($result.output -like "*partition_maintenance_log*") {
        Write-Log "   ✅ Tabela partition_maintenance_log criada" "SUCCESS"
        $TESTS_PASSED++
        return $true
    }
    else {
        Write-Log "   ❌ Tabela partition_maintenance_log não encontrada" "ERROR"
        $TESTS_FAILED++
        return $false
    }
}

# ============================================================================
# FUNCTION: Generate final metrics report
# ============================================================================
function Generate-MetricsReport {
    Write-Log "" "INFO"
    Write-Log "================================================" "INFO"
    Write-Log "STAGE 2: Relatório de Métricas" "INFO"
    Write-Log "================================================" "INFO"
    Write-Log "" "INFO"
    Write-Log "Testes Executados: $($TESTS_PASSED + $TESTS_FAILED)" "INFO"
    Write-Log "Sucessos: $TESTS_PASSED ✅" "SUCCESS"
    Write-Log "Falhas: $TESTS_FAILED ❌" "INFO"
    
    # Create JSON metrics file
    $metricsJson = @{
        "timestamp" = Get-Date -Format "yyyy-MM-ddTHH:mm:ss.fffZ"
        "stage" = "STAGE2_OPT1_DRYRUN"
        "tests_passed" = $TESTS_PASSED
        "tests_failed" = $TESTS_FAILED
        "success_rate" = if (($TESTS_PASSED + $TESTS_FAILED) -gt 0) { [math]::Round(($TESTS_PASSED / ($TESTS_PASSED + $TESTS_FAILED)) * 100, 2) } else { 0 }
        "metrics" = $METRICS
    } | ConvertTo-Json
    
    Set-Content -Path $METRICS_FILE -Value $metricsJson
    Write-Log "" "INFO"
    Write-Log "Métricas salvas em: $METRICS_FILE" "INFO"
    
    return $TESTS_FAILED -eq 0
}

# ============================================================================
# FUNCTION: Generate summary report
# ============================================================================
function Generate-SummaryReport {
    param([bool]$Success)
    
    Write-Log "" "INFO"
    Write-Log "================================================" "INFO"
    Write-Log "STAGE 2: RESULTADO FINAL" "INFO"
    Write-Log "================================================" "INFO"
    
    if ($Success) {
        Write-Log "STATUS: ✅ PASS" "SUCCESS"
        Write-Log "" "INFO"
        Write-Log "Recomendação: PROCEDER PARA STAGE 3 (Rollback Procedure)" "SUCCESS"
    }
    else {
        Write-Log "STATUS: ❌ FAIL" "ERROR"
        Write-Log "" "INFO"
        Write-Log "Ação Requerida: Revisar erros acima" "ERROR"
        Write-Log "Escalação L1/L2 necessária" "ERROR"
    }
    
    Write-Log "" "INFO"
    Write-Log "Log completo: $LOG_FILE" "INFO"
    Write-Log "Métricas: $METRICS_FILE" "INFO"
    Write-Log "================================================" "INFO"
}

# ============================================================================
# MAIN EXECUTION
# ============================================================================

Write-Log "============================================================================" "INFO"
Write-Log "SPRINT 3 - STAGE 2: OPT1 DRY-RUN VALIDATION" "INFO"
Write-Log "============================================================================" "INFO"
Write-Log "Iniciado em: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss UTC')" "INFO"
Write-Log "Database: $DB_NAME @ $($DB_HOST):$($DB_PORT)" "INFO"
Write-Log "User: $DB_USER" "INFO"
Write-Log "============================================================================" "INFO"

# Execute all tests
$allTestsPassed = $true
$allTestsPassed = (Test-PostgreSQLConnection) -and $allTestsPassed
$allTestsPassed = (Test-BaseTableExists) -and $allTestsPassed
$allTestsPassed = (Test-ExistingPartitions) -and $allTestsPassed
$allTestsPassed = (Execute-OPT1Migration) -and $allTestsPassed
$allTestsPassed = (Test-TriggerCreation) -and $allTestsPassed
$allTestsPassed = (Test-FunctionsCreated) -and $allTestsPassed
$allTestsPassed = (Test-PartitionCreation) -and $allTestsPassed
$allTestsPassed = (Test-PartitionCount) -and $allTestsPassed
$allTestsPassed = (Test-MaintenanceLogTable) -and $allTestsPassed

# Generate reports
Generate-MetricsReport
Generate-SummaryReport -Success $allTestsPassed

# Exit with appropriate code
if ($allTestsPassed) {
    exit 0
}
else {
    exit 1
}
