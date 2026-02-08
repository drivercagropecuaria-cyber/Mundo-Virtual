# Plano de limpeza e organizacao

Data: 2026-02-07

## Estrutura canonica proposta

```text
/docs
  /foundation
  /ops
  /architecture
/db
  /migrations
  /sql
/scripts
  /gis
  /ops
  repo_cleanup.ps1
/reports
  (somente relatorios canonicos)
/data
  /raw
  /processed
  /exports
  /samples
/archives/YYYY-MM-DD
  /zips
  /venv
  /logs
  /metrics
  /shadow
  /legacy_projects
  /backups_raw
```

## Fonte de verdade (docs canonicos)

- ../docs/START_HERE.md: comandos oficiais de execucao
- ../docs/INDEX.md: indice de documentos e relatorios

## Tabela de movimentacao (primeira passada)

| atual | destino | acao | justificativa |
| --- | --- | --- | --- |
| archives/2026-02-07/zips/archives/2026-02-07/zips/.github.zip | archives/2026-02-07/zips | ARCHIVE | snapshot duplicado |
| archives/2026-02-07/zips/archives/2026-02-07/zips/.vscode.zip | archives/2026-02-07/zips | ARCHIVE | snapshot duplicado |
| archives/2026-02-07/venv/archives/2026-02-07/zips/archives/2026-02-07/venv/archives/2026-02-07/zips/.venv.zip | archives/2026-02-07/venv | ARCHIVE | ambiente duplicado |
| archives/2026-02-07/venv/archives/2026-02-07/venv/archives/2026-02-07/zips/archives/2026-02-07/venv/archives/2026-02-07/venv/archives/2026-02-07/zips/.venv-gis.zip | archives/2026-02-07/venv | ARCHIVE | ambiente duplicado |
| archives/2026-02-07/zips/archives/2026-02-07/zips/BIBLIOTECA.zip | archives/2026-02-07/zips | ARCHIVE | snapshot duplicado |
| Documentacao Auxiliar  Mundo Virtual Villa.zip | archives/2026-02-07/zips | ARCHIVE | snapshot duplicado |
| archives/2026-02-07/zips/archives/2026-02-07/zips/_kml_test.zip | archives/2026-02-07/zips | ARCHIVE | snapshot de teste |
| archives/2026-02-07/venv/archives/2026-02-07/venv/.venv/ | archives/2026-02-07/venv | ARCHIVE | ambiente local |
| archives/2026-02-07/venv/archives/2026-02-07/venv/archives/2026-02-07/venv/archives/2026-02-07/venv/.venv-gis/ | archives/2026-02-07/venv | ARCHIVE | ambiente local |
| archives/2026-02-07/shadow/archives/2026-02-07/shadow/shadow_deployment_results/ | archives/2026-02-07/shadow | ARCHIVE | evidencias antigas |
| archives/2026-02-07/backups_raw/backup_villa_canabrava.sql | archives/2026-02-07/backups_raw | ARCHIVE | backup solto no root |
| archives/2026-02-07/backups_raw/geometrias_dump_FEB6.sql | archives/2026-02-07/backups_raw | ARCHIVE | backup solto no root |
| METRICS_*.json | archives/2026-02-07/metrics | ARCHIVE | metrics antigas |
| METRICS_*.txt | archives/2026-02-07/metrics | ARCHIVE | logs de metrics |
| STAGE*_LOG*.txt | archives/2026-02-07/logs | ARCHIVE | logs de execucao |
| archives/2026-02-07/logs/gis_async_pipeline*.log | archives/2026-02-07/logs | ARCHIVE | logs de pipeline |
| EXEC_REPORT_*.md | archives/2026-02-07/logs | ARCHIVE | relatorios de execucao antigos |
| STAGE*_*.md | archives/2026-02-07/logs | ARCHIVE | relatorios de execucao |
| archives/2026-02-07/logs/REPORT_ULTIMOS_25_COMANDOS_RAW.txt | archives/2026-02-07/logs | ARCHIVE | log bruto |
| REPORT_ULTIMOS_25_COMANDOS.md | reports | KEEP | relatorio canonico |
| README_EXECUCAO.md | docs/ops | MOVE | guia de execucao |
| docker-compose.yml | root | KEEP | infra canonica |
| .env.example | root | KEEP | configuracao canonica |
| docs/ENV.md | docs/ops | MOVE | documentacao de ambiente |
| scripts/gis/* | scripts/gis | KEEP | scripts canonicos |
| reports/*.md | reports | KEEP | relatorios canonicos |
| exports/geojson | data/exports/geojson | MOVE (fase 2) | consolidar dados |
| Villa_Canabrava_Digital_World/ | archives/2026-02-07/legacy_projects | ARCHIVE | subprojeto legado |
| BIBLIOTECA_git_backup/ | archives/2026-02-07/legacy_projects | ARCHIVE | backup legado |

## Riscos

- Mover archives/2026-02-07/venv/archives/2026-02-07/venv/.venv pode exigir recriar ambiente local.
- Mover exports pode exigir atualizar caminhos em relatorios.
- Subprojetos podem conter arquivos ainda uteis; por isso vao para archives.

## Criterios objetivos de "nao presta" no root

- Zips de snapshot de pastas existentes.
- Logs e relatorios de execucao antigos.
- Ambientes virtuais versionados.
- Backups SQL soltos.

## Observacoes

- Nenhuma delecao definitiva nesta fase.
- Tudo suspeito vai para /archives/YYYY-MM-DD.
- Subprojetos legados sao excluidos quando -ExcludeLegacy estiver ativo.




