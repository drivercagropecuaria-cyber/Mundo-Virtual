# README_EXECUCAO

## Pipeline unico (1 comando)

```powershell
copy .env.example .env
.\scripts\run_pipeline.ps1 -KmlDir "C:\Users\rober\Downloads\KML\KML" -OutDir "out"
```

Para resetar o banco (somente quando explicitado):

```powershell
.\scripts\run_pipeline.ps1 -KmlDir "C:\Users\rober\Downloads\KML\KML" -OutDir "out" -Reset
```

Observacao: o pipeline instala dependencias Python a partir de requirements-gis.txt se necessario.

## 1) Subir infraestrutura

```powershell
copy .env.example .env
# ajuste POSTGRES_USER/POSTGRES_PASSWORD/POSTGRES_DB/POSTGRES_PORT se necessario
# porta sugerida: 15433 (evita conflito com postgres_test em 15432)

docker compose up -d
```

## 2) Backup antes de migracoes

```powershell
# salva backup do banco (nao destrutivo)
docker exec -i villa_canabrava_postgis pg_dump -U postgres -d villa_canabrava > archives/2026-02-07/backups_raw/backup_villa_canabrava.sql
```

## 3) Rodar migracoes

```powershell
Get-Content db/migrations/0001_init.sql -Raw | docker exec -i villa_canabrava_postgis psql -U postgres -d villa_canabrava -v ON_ERROR_STOP=1
Get-Content db/migrations/0002_idempotency.sql -Raw | docker exec -i villa_canabrava_postgis psql -U postgres -d villa_canabrava -v ON_ERROR_STOP=1
Get-Content db/migrations/0003_gis_data.sql -Raw | docker exec -i villa_canabrava_postgis psql -U postgres -d villa_canabrava -v ON_ERROR_STOP=1
```

## 4) Importar KML/KMZ

```powershell
# exemplo com variaveis de ambiente
$env:DB_HOST = "localhost"
$env:DB_PORT = "15433"
$env:DB_NAME = "villa_canabrava"
$env:DB_USER = "postgres"
$env:DB_PASSWORD = "postgres"

python scripts/gis/import_kml_to_postgis.py --kml-dir "C:\Users\rober\Downloads\KML\KML" --schema villa_canabrava --summary-out import_summary.json --report-dir reports --no-replace
```

## 5) Validar dados e gerar relatorio

```powershell
python scripts/gis/validate_pipeline.py --schema villa_canabrava --contract data/contract/villa_canabrava_contract.json --out-manifest out/golden/manifest.json --out-report out/reports/validation_report.md --strict
```

## 6) Exportar GeoJSON por camada

```powershell
python scripts/gis/export_geojson_from_postgis.py --schema villa_canabrava --output-dir out/golden --report-out out/reports/export_report.md
```

## 6) (Opcional) Tileserver GL

Crie uma pasta `tileserver` e adicione o config do TileServer GL apontando para um arquivo MBTiles do schema `villa_canabrava`. Esse passo nao e necessario para a importacao/validacao.




