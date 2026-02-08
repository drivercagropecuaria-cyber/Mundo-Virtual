param(
    [string]$ArchiveDate = (Get-Date -Format "yyyy-MM-dd"),
    [switch]$WhatIf = $true,
    [switch]$ExcludeLegacy = $true,
    [string]$LogPath = (Join-Path (Join-Path $PSScriptRoot "..") "reports/cleanup_run.log")
)

$ErrorActionPreference = "Stop"

$root = Resolve-Path (Join-Path $PSScriptRoot "..")
$archives = Join-Path $root "archives/$ArchiveDate"
$reportDir = Join-Path $root "reports"
$logPath = $LogPath

$subdirs = @(
    "zips",
    "venv",
    "logs",
    "metrics",
    "shadow",
    "legacy_projects",
    "backups_raw"
)

function Write-Log {
    param([string]$Message)
    $ts = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $line = "[$ts] $Message"
    Add-Content -Path $logPath -Value $line
}

function Ensure-Dir {
    param([string]$Path)
    if (-not (Test-Path $Path)) {
        New-Item -ItemType Directory -Path $Path | Out-Null
    }
}

function Move-Safe {
    param([string]$Path, [string]$DestDir)
    if (-not (Test-Path $Path)) {
        return
    }
    Ensure-Dir $DestDir
    $dest = Join-Path $DestDir (Split-Path $Path -Leaf)
    if ($WhatIf) {
        Write-Host "[WHATIF] Move $Path -> $dest"
        Write-Log "WHATIF Move $Path -> $dest"
    } else {
        Move-Item -Path $Path -Destination $dest
        Write-Log "Move $Path -> $dest"
    }
}

Ensure-Dir $reportDir
Ensure-Dir $archives
foreach ($name in $subdirs) {
    Ensure-Dir (Join-Path $archives $name)
}

Write-Log "START cleanup"
Write-Log "Root: $root"
Write-Log "Archives: $archives"
Write-Log "WhatIf: $WhatIf"
Write-Log "ExcludeLegacy: $ExcludeLegacy"

# Zips no root
Get-ChildItem -Path $root -Filter "*.zip" -File | ForEach-Object {
    Move-Safe $_.FullName (Join-Path $archives "zips")
}

# Venvs no root
Move-Safe (Join-Path $root "archives/2026-02-07/venv/archives/2026-02-07/venv/.venv") (Join-Path $archives "venv")
Move-Safe (Join-Path $root "archives/2026-02-07/venv/archives/2026-02-07/venv/archives/2026-02-07/venv/archives/2026-02-07/venv/.venv-gis") (Join-Path $archives "venv")

# Backups soltos
Move-Safe (Join-Path $root "archives/2026-02-07/backups_raw/backup_villa_canabrava.sql") (Join-Path $archives "backups_raw")
Move-Safe (Join-Path $root "archives/2026-02-07/backups_raw/geometrias_dump_FEB6.sql") (Join-Path $archives "backups_raw")

# Logs e metrics no root
Get-ChildItem -Path $root -Filter "*.log" -File | ForEach-Object {
    Move-Safe $_.FullName (Join-Path $archives "logs")
}
Get-ChildItem -Path $root -Filter "METRICS_*.json" -File | ForEach-Object {
    Move-Safe $_.FullName (Join-Path $archives "metrics")
}
Get-ChildItem -Path $root -Filter "METRICS_*.txt" -File | ForEach-Object {
    Move-Safe $_.FullName (Join-Path $archives "metrics")
}
Get-ChildItem -Path $root -Filter "STAGE*_LOG*.txt" -File | ForEach-Object {
    Move-Safe $_.FullName (Join-Path $archives "logs")
}
Move-Safe (Join-Path $root "archives/2026-02-07/logs/REPORT_ULTIMOS_25_COMANDOS_RAW.txt") (Join-Path $archives "logs")
Get-ChildItem -Path $root -Filter "EXEC_REPORT_*.md" -File | ForEach-Object {
    Move-Safe $_.FullName (Join-Path $archives "logs")
}
Get-ChildItem -Path $root -Filter "STAGE*_*.md" -File | ForEach-Object {
    Move-Safe $_.FullName (Join-Path $archives "logs")
}

# Pasta de evidencias de shadow deployment
Move-Safe (Join-Path $root "archives/2026-02-07/shadow/archives/2026-02-07/shadow/shadow_deployment_results") (Join-Path $archives "shadow")

# Subprojetos legados
if ($ExcludeLegacy) {
    Write-Log "SKIP (ExcludeLegacy) Villa_Canabrava_Digital_World"
    Write-Log "SKIP (ExcludeLegacy) BIBLIOTECA_git_backup"
} else {
    Move-Safe (Join-Path $root "Villa_Canabrava_Digital_World") (Join-Path $archives "legacy_projects")
    Move-Safe (Join-Path $root "BIBLIOTECA_git_backup") (Join-Path $archives "legacy_projects")
}

Write-Log "END cleanup"
Write-Host "Cleanup finalizado. Log: $logPath"



