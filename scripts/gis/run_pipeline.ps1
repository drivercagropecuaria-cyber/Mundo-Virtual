param(
    [string]$KmlDir = "C:\Users\rober\Downloads\KML\KML",
    [string]$Schema = "villa_canabrava"
)

$ErrorActionPreference = "Stop"

function Load-EnvFile {
    param([string]$Path)
    if (-not (Test-Path $Path)) {
        return
    }
    Get-Content $Path | ForEach-Object {
        $line = $_.Trim()
        if ($line -eq "" -or $line.StartsWith("#")) {
            return
        }
        $parts = $line.Split("=", 2)
        if ($parts.Count -eq 2) {
            $name = $parts[0].Trim()
            $value = $parts[1].Trim()
            if ($name -ne "") {
                Set-Item -Path ("env:" + $name) -Value $value
            }
        }
    }
}

$root = Resolve-Path (Join-Path $PSScriptRoot "..\..")
$envFile = Join-Path $root ".env"
Load-EnvFile $envFile

$reportsDir = Join-Path $root "reports"
$exportsDir = Join-Path $root "exports\geojson"

if (-not (Test-Path $reportsDir)) { New-Item -ItemType Directory -Path $reportsDir | Out-Null }
if (-not (Test-Path $exportsDir)) { New-Item -ItemType Directory -Path $exportsDir | Out-Null }

$pythonExe = "python"
if ($env:PYTHON_EXE) {
    $pythonExe = $env:PYTHON_EXE
}

& $pythonExe (Join-Path $PSScriptRoot "import_kml_to_postgis.py") --kml-dir $KmlDir --schema $Schema --summary-out (Join-Path $root "import_summary.json") --report-dir $reportsDir --replace-existing
& $pythonExe (Join-Path $PSScriptRoot "validate_db.py") --schema $Schema --output (Join-Path $root "validation_report.md") --quality-out (Join-Path $reportsDir "03_spatial_quality.md")
& $pythonExe (Join-Path $PSScriptRoot "export_geojson_from_postgis.py") --schema $Schema --output-dir $exportsDir --report-out (Join-Path $reportsDir "05_export.md")
