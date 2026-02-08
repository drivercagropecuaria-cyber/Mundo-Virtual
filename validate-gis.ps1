param(
  [string]$VenvPath = "archives/2026-02-07/venv/archives/2026-02-07/venv/archives/2026-02-07/venv/archives/2026-02-07/venv/.venv-gis"
)

$pythonExe = Join-Path $VenvPath "Scripts\python.exe"
if (-not (Test-Path $pythonExe)) {
  Write-Error "Python not found at $pythonExe. Create the GIS venv first."
  exit 1
}

$code = "import geopandas as gpd; import shapely; import fiona; import pyproj; " +
  "print('geopandas=' + gpd.__version__); " +
  "print('shapely=' + shapely.__version__); " +
  "print('fiona=' + fiona.__version__); " +
  "print('pyproj=' + pyproj.__version__)"

& $pythonExe -c $code
if ($LASTEXITCODE -ne 0) {
  exit $LASTEXITCODE
}

Write-Host "GIS environment OK."


