# STAGING DEPLOY SCRIPT - WEEK 1
# Sprint 3 staging deployment (manual/controlled)

param(
    [string]$DbHost = "host.docker.internal",
    [int]$DbPort = 5432,
    [string]$DbName = "BIBLIOTECA",
    [string]$DbUser = "postgres",
    [string]$DbPassword = ""
)

$ErrorActionPreference = "Stop"

Write-Host "[STAGING] Pre-flight connection check..."
& "$env:ProgramFiles\PostgreSQL\15\bin\psql.exe" -h $DbHost -p $DbPort -U $DbUser -d $DbName -c "SELECT version();" 

Write-Host "[STAGING] Backup database..."
& "$env:ProgramFiles\PostgreSQL\15\bin\pg_dump.exe" -h $DbHost -p $DbPort -U $DbUser -d $DbName -F c -f "${DbName}_backup_week1.dump"

Write-Host "[STAGING] Apply OPT1 migration..."
& "$env:ProgramFiles\PostgreSQL\15\bin\psql.exe" -h $DbHost -p $DbPort -U $DbUser -d $DbName -f "BIBLIOTECA/supabase/migrations/1770470100_temporal_partitioning_geometrias.sql"

Write-Host "[STAGING] Validate partitions..."
& "$env:ProgramFiles\PostgreSQL\15\bin\psql.exe" -h $DbHost -p $DbPort -U $DbUser -d $DbName -c "SELECT schemaname, tablename FROM pg_tables WHERE tablename LIKE 'geometrias%';"

Write-Host "[STAGING] Collect OPT1 metrics..."
$env:DB_HOST = $DbHost
$env:DB_PORT = $DbPort
$env:DB_NAME = $DbName
$env:DB_USER = $DbUser
$env:DB_PASSWORD = $DbPassword
& "c:/Users/rober/Desktop/MUNDO VIRTUAL VILLA CANABRAVA/archives/2026-02-07/venv/archives/2026-02-07/venv/.venv/Scripts/python.exe" "collect_opt1_metrics.py"

Write-Host "[STAGING] Done. Review outputs and monitoring."


