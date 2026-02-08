# Evidence collection helper for Sprint/Pre-Flight
# Usage: .\collect_evidence.ps1 -PreFlightLogPath <path> -BoundsReportPath <path> -ExecReportPath <path>
# Outputs a ready-to-paste evidence block

param(
    [Parameter(Mandatory = $true)]
    [string]$PreFlightLogPath,
    [Parameter(Mandatory = $true)]
    [string]$BoundsReportPath,
    [Parameter(Mandatory = $true)]
    [string]$RpcLogPath,
    [Parameter(Mandatory = $true)]
    [string]$ExecReportPath,
    [Parameter(Mandatory = $false)]
    [string]$GeometryReportPath = "BIBLIOTECA/reports/DB_VALIDATION_REPORT_POST_REMEDIATION.json",
    [Parameter(Mandatory = $false)]
    [string[]]$MigrationPaths = @(
        "BIBLIOTECA/supabase/migrations/1770369200_fix_all_views_catalogo_rename.sql",
        "BIBLIOTECA/supabase/migrations/1770201200_update_catalogo_view_proxy.sql",
        "BIBLIOTECA/supabase/migrations/1770169200_optimize_search_catalogo.sql"
    ),
    [Parameter(Mandatory = $false)]
    [string]$AsyncPipelinePath = "gis_async_geometry_validator.py"
)

function Resolve-RepoPath([string]$path) {
    if (Test-Path $path) {
        $full = Resolve-Path $path
        $cwd = (Get-Location).Path
        return $full.Path.Replace($cwd + "\", "").Replace("\\", "/")
    }
    return $path.Replace("\\", "/")
}

$timestamp = (Get-Date).ToString("yyyy-MM-ddTHH:mm:ssK")
$preflightRel = Resolve-RepoPath $PreFlightLogPath
$boundsRel = Resolve-RepoPath $BoundsReportPath
$rpcRel = Resolve-RepoPath $RpcLogPath
$execRel = Resolve-RepoPath $ExecReportPath
$geometryRel = Resolve-RepoPath $GeometryReportPath
$asyncRel = Resolve-RepoPath $AsyncPipelinePath
$migrationsRel = $MigrationPaths | ForEach-Object { Resolve-RepoPath $_ }

$block = @()
$block += "## EVIDENCIAS (PADRAO)"
$block += "- **Pre-Flight**: [$preflightRel]($preflightRel)"
$block += "- **GIS Bounds**: [$boundsRel]($boundsRel)"
$block += "- **RPCs (logs/outputs)**: [$rpcRel]($rpcRel)"
$block += "- **JSON Geometria**: [$geometryRel]($geometryRel)"
$block += "- **Migrations**:"
$migrationsRel | ForEach-Object { $block += "  - [$_]($_)" }
$block += "- **Pipeline GIS Assincrona (v1)**: [$asyncRel]($asyncRel)"
$block += "- **EXEC_REPORT**: [$execRel]($execRel)"
$block += "- **Timestamp**: $timestamp"

Write-Host ""; Write-Host ($block -join "`n")
