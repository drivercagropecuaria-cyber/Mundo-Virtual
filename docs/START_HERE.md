# Start here

Este documento resume como rodar o ambiente canonico e onde estao os artefatos principais.
Todos os comandos abaixo funcionam no PowerShell sem exigir `psql` instalado localmente.

## Caminho canonico de execucao

### Pipeline unico (1 comando)

```powershell
copy .env.example .env
.\scripts\run_pipeline.ps1 -KmlDir "C:\Users\rober\Downloads\KML\KML" -OutDir "out"
```

Para resetar o banco (somente quando explicitado):

```powershell
.\scripts\run_pipeline.ps1 -KmlDir "C:\Users\rober\Downloads\KML\KML" -OutDir "out" -Reset
```

1) Subir o PostGIS

```powershell
copy .env.example .env
# ajuste se necessario

docker compose up -d
```

2) Rodar migracoes

```powershell
Get-Content db/migrations/0001_init.sql -Raw | docker exec -i villa_canabrava_postgis psql -U postgres -d villa_canabrava -v ON_ERROR_STOP=1
Get-Content db/migrations/0002_idempotency.sql -Raw | docker exec -i villa_canabrava_postgis psql -U postgres -d villa_canabrava -v ON_ERROR_STOP=1
Get-Content db/migrations/0003_gis_data.sql -Raw | docker exec -i villa_canabrava_postgis psql -U postgres -d villa_canabrava -v ON_ERROR_STOP=1
```

3) Pipeline GIS (importar, validar, exportar)

```powershell
## 3.1) Importacao (dry-run)
python scripts/gis/import_kml_to_postgis.py --kml-dir "C:\Users\rober\Downloads\KML\KML" --schema villa_canabrava --dry-run --report-dir reports

## 3.2) Importacao (full, idempotente, sem reset)
python scripts/gis/import_kml_to_postgis.py --kml-dir "C:\Users\rober\Downloads\KML\KML" --schema villa_canabrava --summary-out import_summary.json --report-dir reports --no-replace

## 3.3) Exportacao
python scripts/gis/export_geojson_from_postgis.py --schema villa_canabrava --output-dir out/golden --report-out out/reports/export_report.md

## 3.4) Validacao
python scripts/gis/validate_pipeline.py --schema villa_canabrava --contract data/contract/villa_canabrava_contract.json --out-manifest out/golden/manifest.json --out-report out/reports/validation_report.md --strict
```

## Onde estao as evidencias

- Relatorios canonicos: `reports/`
- Golden outputs: `out/golden/`
- Relatorios do pipeline: `out/reports/validation_report.md`
- Inventario e plano de limpeza: `reports/00_repo_inventory.md` e `reports/01_cleanup_plan.md`
- Arquivos antigos: `archives/YYYY-MM-DD/`

## Observacoes

- Porta canonica: 15433
- Schema principal: `villa_canabrava`
- Dependencias Python: requirements-gis.txt (instaladas automaticamente pelo pipeline)
