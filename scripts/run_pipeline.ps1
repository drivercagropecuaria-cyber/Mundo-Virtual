param(
    [string]$KmlDir = $env:KML_DIR,
    [string]$OutDir = "out",
    [switch]$Reset
)

$ErrorActionPreference = "Stop"

function Import-DotEnv {
    param(
        [Parameter(Mandatory = $true)]
        [string]$EnvPath
    )

    if (-not (Test-Path $EnvPath)) {
        Write-Host "[env] .env nao encontrado: $EnvPath (ok se nao for necessario)"
        return
    }

    Write-Host "[env] Carregando: $EnvPath"
    Get-Content $EnvPath | ForEach-Object {
        $line = $_.Trim()

        if (-not $line) { return }
        if ($line.StartsWith("#")) { return }

        $m = [regex]::Match($line, '^\s*([A-Za-z_][A-Za-z0-9_]*)\s*=\s*(.*)\s*$')
        if (-not $m.Success) { return }

        $name = $m.Groups[1].Value
        $value = $m.Groups[2].Value

        if ([string]::IsNullOrWhiteSpace($name)) { return }

        if (($value.StartsWith('"') -and $value.EndsWith('"')) -or ($value.StartsWith("'") -and $value.EndsWith("'"))) {
            $value = $value.Substring(1, $value.Length - 2)
        }

        Set-Item -Path ("Env:{0}" -f $name) -Value $value
    }
}

function Invoke-Checked {
    param([scriptblock]$Command, [string]$ErrorMessage)
    & $Command
    if ($LASTEXITCODE -ne 0) {
        throw $ErrorMessage
    }
}

function Invoke-PsqlFile {
    param(
        [string]$FilePath,
        [string]$DbUser,
        [string]$DbName
    )
    if (-not (Test-Path $FilePath)) {
        throw "Migration file not found: $FilePath"
    }
    $sql = Get-Content -Raw -Path $FilePath
    $sql | docker exec -i villa_canabrava_postgis psql -U $DbUser -d $DbName -v ON_ERROR_STOP=1
    if ($LASTEXITCODE -ne 0) {
        throw "psql failed for $FilePath"
    }
}

function Wait-ContainerHealthy {
    param(
        [string]$ContainerName,
        [int]$MaxAttempts = 24,
        [int]$DelaySeconds = 5
    )
    for ($i = 0; $i -lt $MaxAttempts; $i++) {
        $status = docker inspect $ContainerName --format "{{.State.Health.Status}}" 2>$null
        if ($status -eq "healthy") {
            return
        }
        Start-Sleep -Seconds $DelaySeconds
    }
    throw "Container $ContainerName not healthy after $MaxAttempts attempts."
}

$repoRoot = Resolve-Path (Join-Path $PSScriptRoot "..")
Import-DotEnv -EnvPath (Join-Path $repoRoot ".env")

$pythonExe = "python"
if ($env:PYTHON_EXE) {
    $pythonExe = $env:PYTHON_EXE
}

$dbUser = $env:DB_USER
if (-not $dbUser) { $dbUser = "postgres" }
$dbName = $env:DB_NAME
if (-not $dbName) { $dbName = "villa_canabrava" }

if (-not $KmlDir -or $KmlDir -eq "") {
    $KmlDir = "C:\Users\rober\Downloads\KML\KML"
}

$contractPath = Join-Path $repoRoot "data\contract\villa_canabrava_contract.json"
$reportsDir = Join-Path $repoRoot (Join-Path $OutDir "reports")
$goldenDir = Join-Path $repoRoot (Join-Path $OutDir "golden")
$manifestPath = Join-Path $goldenDir "manifest.json"
$validationReport = Join-Path $reportsDir "validation_report.md"

if (-not (Test-Path $reportsDir)) { New-Item -ItemType Directory -Path $reportsDir | Out-Null }
if (-not (Test-Path $goldenDir)) { New-Item -ItemType Directory -Path $goldenDir | Out-Null }

Write-Host "[1/5] Subindo PostGIS..."
Invoke-Checked { docker compose up -d } "docker compose failed"
Wait-ContainerHealthy -ContainerName "villa_canabrava_postgis"

Write-Host "[2/5] Rodando migracoes..."
Invoke-PsqlFile "db/migrations/0001_init.sql" $dbUser $dbName
Invoke-PsqlFile "db/migrations/0002_idempotency.sql" $dbUser $dbName
Invoke-PsqlFile "db/migrations/0003_gis_data.sql" $dbUser $dbName

if ($Reset) {
    Write-Host "[2.1] Reset explicitado: limpando dados..."
    Invoke-Checked { docker exec -i villa_canabrava_postgis psql -U $dbUser -d $dbName -c "TRUNCATE TABLE villa_canabrava.geo_features, villa_canabrava.layers RESTART IDENTITY;" } "Reset failed on villa_canabrava"
    Invoke-Checked { docker exec -i villa_canabrava_postgis psql -U $dbUser -d $dbName -c "TRUNCATE TABLE gis_data.features RESTART IDENTITY;" } "Reset failed on gis_data"
}

Write-Host "[2.5] Verificando dependencias Python..."
$requirements = Join-Path $root "requirements-gis.txt"
$prevErrorAction = $ErrorActionPreference
$ErrorActionPreference = "Continue"
& $pythonExe -c "import fiona, shapely, pyproj, psycopg2" 2>$null
$depOk = ($LASTEXITCODE -eq 0)
$ErrorActionPreference = $prevErrorAction
if (-not $depOk) {
    if (-not (Test-Path $requirements)) {
        throw "requirements-gis.txt not found"
    }
    Invoke-Checked { & $pythonExe -m pip install -r $requirements } "pip install requirements-gis.txt failed"
}

Write-Host "[3/5] Importando KML/KMZ..."
$importArgs = @(
    "--kml-dir", $KmlDir,
    "--schema", "villa_canabrava",
    "--summary-out", (Join-Path $repoRoot "import_summary.json"),
    "--report-dir", (Join-Path $repoRoot "reports")
)
if ($Reset) {
    $importArgs += "--replace-existing"
} else {
    $importArgs += "--no-replace"
}

Invoke-Checked { & $pythonExe (Join-Path $repoRoot "scripts\gis\import_kml_to_postgis.py") @importArgs } "import_kml_to_postgis failed"

Write-Host "[4/5] Exportando GeoJSON (golden)..."
Invoke-Checked { & $pythonExe (Join-Path $repoRoot "scripts\gis\export_geojson_from_postgis.py") --schema villa_canabrava --output-dir $goldenDir --report-out (Join-Path $reportsDir "export_report.md") } "export_geojson_from_postgis failed"

Write-Host "[5/5] Validando contrato + gerando manifest/report..."
Invoke-Checked { & $pythonExe (Join-Path $repoRoot "scripts\gis\validate_pipeline.py") --schema villa_canabrava --contract $contractPath --out-manifest $manifestPath --out-report $validationReport --strict } "validate_pipeline failed"

Write-Host "Pipeline finalizado."
Write-Host "Golden: $goldenDir"
Write-Host "Manifest: $manifestPath"
Write-Host "Report: $validationReport"
