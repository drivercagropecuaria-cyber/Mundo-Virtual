# EXEC_REPORT - Shadow Deploy Validator + GIS Env

## Scope
- Add formal shadow deploy validator script for frontend.
- Standardize GIS Python environment with requirements and validation script.

## Artifacts
- Validator script: BIBLIOTECA/frontend/scripts/validate-shadow-deploy.mjs
- NPM script: BIBLIOTECA/frontend/package.json (validate:shadow)
- GIS requirements: requirements-gis.txt
- GIS validation: validate-gis.ps1

## Commands Executed (Evidence)
- Create GIS venv:
  - Command: "c:/Users/rober/Desktop/MUNDO VIRTUAL VILLA CANABRAVA/.VENV/Scripts/python.exe" -m venv .venv-gis
  - Result: OK
- Install GIS dependencies:
  - Command: .\.venv-gis\Scripts\python.exe -m pip install -r requirements-gis.txt
  - Result: OK (geopandas, shapely, fiona, pyproj)
- Validate GIS imports:
  - Command: .\validate-gis.ps1
  - Result: OK (geopandas=1.1.2, shapely=2.1.2, fiona=1.10.1, pyproj=3.7.1)

## Notes
- Shadow deploy validator script was added but not executed in this run.
- Build output detection defaults to Vite (dist/) when the build script includes vite.
- Supabase env validation uses aliases and blocks service-role keys in frontend.
