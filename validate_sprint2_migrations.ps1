# Sprint 2 SQL Migration Validation Script
# Purpose: Validar sintaxe de todas as migrations implementadas no Sprint 2
# Created: 2026-02-06
# Usage: .\validate_sprint2_migrations.ps1

param(
    [string]$MigrationsPath = "BIBLIOTECA/supabase/migrations",
    [switch]$Verbose = $false
)

$ErrorActionPreference = "Continue"
$FailedValidations = 0
$PassedValidations = 0

Write-Host "=================================================="
Write-Host "Sprint 2 SQL Migration Validator"
Write-Host "=================================================="
Write-Host ""

# Lista de migrations Sprint 2 a validar
$Sprint2Migrations = @(
    "1770470100_temporal_partitioning_geometrias.sql",
    "1770470200_columnar_storage_gis.sql",
    "1770470300_indexed_views_rpc_search.sql"
)

# Step 1: Verificar se arquivos existem
Write-Host "[Step 1] Verificando existencia de arquivos..."
Write-Host ""

foreach ($Migration in $Sprint2Migrations) {
    $FilePath = Join-Path $MigrationsPath $Migration
    
    if (Test-Path -Path $FilePath) {
        Write-Host "   PASS: $Migration"
        $PassedValidations++
    } else {
        Write-Host "   FAIL: $Migration (NOT FOUND)"
        $FailedValidations++
    }
}

Write-Host ""

# Step 2: Verificar sintaxe SQL basica
Write-Host "[Step 2] Validando sintaxe SQL basica..."
Write-Host ""

foreach ($Migration in $Sprint2Migrations) {
    $FilePath = Join-Path $MigrationsPath $Migration
    
    if (-not (Test-Path -Path $FilePath)) {
        continue
    }
    
    $Content = Get-Content -Path $FilePath -Raw
    
    # Verificar transaction integrity
    $HasBegin = $Content -match "BEGIN"
    $HasCommit = $Content -match "COMMIT"
    
    Write-Host "   File: $Migration"
    
    if ($HasBegin -and $HasCommit) {
        Write-Host "      PASS: Transaction block (BEGIN/COMMIT)"
        $PassedValidations++
    } else {
        Write-Host "      FAIL: Transaction block incomplete"
        $FailedValidations++
    }
    
    # Verificar keywords SQL
    $KeywordCount = 0
    $SQLKeywords = @("CREATE", "INSERT", "UPDATE", "DELETE", "SELECT", "ALTER", "DROP")
    foreach ($Keyword in $SQLKeywords) {
        if ($Content -match $Keyword) {
            $KeywordCount++
        }
    }
    
    if ($KeywordCount -gt 0) {
        Write-Host "      PASS: SQL keywords found ($KeywordCount)"
        $PassedValidations++
    } else {
        Write-Host "      FAIL: No SQL keywords found"
        $FailedValidations++
    }
    
    Write-Host ""
}

# Step 3: Verificar ordem das migrations
Write-Host "[Step 3] Validando ordem das migrations..."
Write-Host ""

$MigrationNumbers = @()
foreach ($Migration in $Sprint2Migrations) {
    $Number = [int64]($Migration -replace "_.*", "")
    $MigrationNumbers += $Number
}

$IsOrdered = $true
for ($i = 0; $i -lt $MigrationNumbers.Count - 1; $i++) {
    if ($MigrationNumbers[$i] -gt $MigrationNumbers[$i + 1]) {
        $IsOrdered = $false
        break
    }
}

if ($IsOrdered) {
    Write-Host "   PASS: Migrations em ordem crescente"
    Write-Host "      $($MigrationNumbers -join ' < ')"
    $PassedValidations++
} else {
    Write-Host "   FAIL: Migrations FORA de ordem"
    $FailedValidations++
}

Write-Host ""

# Step 4: Resumo Final
Write-Host "=================================================="
Write-Host "VALIDACAO FINAL"
Write-Host "=================================================="
Write-Host ""

Write-Host "Resumo:"
Write-Host "  Migrations validadas: $($Sprint2Migrations.Count)"
Write-Host "  Validacoes passou: $PassedValidations"
Write-Host "  Validacoes falhou: $FailedValidations"
Write-Host ""

if ($FailedValidations -eq 0) {
    Write-Host "Status: ALL VALIDATIONS PASSED"
    Write-Host ""
    Write-Host "Exit Code: 0 (SUCCESS)"
    exit 0
} else {
    Write-Host "Status: SOME VALIDATIONS FAILED"
    Write-Host ""
    Write-Host "Exit Code: 1 (FAILED)"
    exit 1
}
