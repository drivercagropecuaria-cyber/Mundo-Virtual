# Relatorio de cenario atual - Mundo Virtual Villa Canabrava

Data: 2026-02-07

## Resumo executivo

- Pipeline unico criado em [scripts/run_pipeline.ps1](../scripts/run_pipeline.ps1) para importacao, exportacao e validacao.
- Contrato canonico definido em [data/contract/villa_canabrava_contract.json](../data/contract/villa_canabrava_contract.json).
- Docker PostGIS configurado via [docker-compose.yml](../docker-compose.yml) com porta 15433.
- Migracoes canonicas em [db/migrations](../db/migrations) com idempotencia.
- Documentacao central em [docs/START_HERE.md](../docs/START_HERE.md) e indice em [docs/INDEX.md](../docs/INDEX.md).

## Estado do pipeline unico

- Entrada principal: [scripts/run_pipeline.ps1](../scripts/run_pipeline.ps1).
- Etapas: subir container, aplicar migracoes, importar KML/KMZ, exportar golden, validar contrato.
- Saidas esperadas:
  - out/golden/*.geojson (golden por layer)
  - out/golden/manifest.json
  - out/reports/validation_report.md
- Idempotencia: importacao usa --no-replace por padrao (somente limpa com -Reset).
- Dependencias Python: requirements-gis.txt (auto-instaladas quando necessario).

## Estado do Docker

- Config: [docker-compose.yml](../docker-compose.yml).
- Servico: postgis/postgis:15-3.3-alpine.
- Container: villa_canabrava_postgis.
- Porta: 127.0.0.1:15433 -> 5432.
- Volume: villa_canabrava_pgdata.
- Observacao: docker compose mostra aviso de atributo version (obsoleto, nao bloqueante).

## Banco e migracoes

- Migracoes canonicas:
  - [db/migrations/0001_init.sql](../db/migrations/0001_init.sql): extensoes e schema villa_canabrava.
  - [db/migrations/0002_idempotency.sql](../db/migrations/0002_idempotency.sql): feature_hash + indice unico.
  - [db/migrations/0003_gis_data.sql](../db/migrations/0003_gis_data.sql): schema gis_data + view de compatibilidade.
- Schema principal: villa_canabrava.
- View compatibilidade: gis_data.geo_features.

## Contrato e validacoes

- Contrato canonico: [data/contract/villa_canabrava_contract.json](../data/contract/villa_canabrava_contract.json).
- Validacoes automaticas (validate_pipeline.py):
  - layers processadas == 252
  - bounds dentro do contrato
  - ST_IsValid = true
  - SRID = 4326
  - duplicatas por (layer_name + feature_hash) bloqueiam strict
  - area/perimetro da camada de perimetro dentro da tolerancia

## Scripts e funcoes principais

- [scripts/run_pipeline.ps1](../scripts/run_pipeline.ps1): orquestracao 1-clique.
- [scripts/gis/import_kml_to_postgis.py](../scripts/gis/import_kml_to_postgis.py): importacao KML/KMZ (doc.kml em KMZ).
- [scripts/gis/export_geojson_from_postgis.py](../scripts/gis/export_geojson_from_postgis.py): exportacao por layer.
- [scripts/gis/validate_pipeline.py](../scripts/gis/validate_pipeline.py): contrato + manifest + report.
- [scripts/gis/run_pipeline.ps1](../scripts/gis/run_pipeline.ps1): runner legado (nao e o pipeline unico).
- [scripts/repo_cleanup.ps1](../scripts/repo_cleanup.ps1): limpeza segura e arquivamento.

## Pastas e uso (alto nivel)

- docs/: documentacao viva e indices.
- scripts/: automacoes (pipeline, GIS, operacao).
- db/: migracoes e SQL canonico.
- data/: dados e contrato.
- reports/: relatorios de governanca e validacao.
- plans/: planos e checklists.
- archives/2026-02-07/: material arquivado (zips, venvs, logs, metrics, backups).
- BIBLIOTECA/: subprojeto legado (mantido no root, nao arquivado nesta rodada).
- Villa_Canabrava_Digital_World/: subprojeto legado (mantido no root, nao arquivado nesta rodada).
- Documentacao Auxiliar  Mundo Virtual Villa/: acervo documental auxiliar.

## Inventario detalhado por pasta (nivel 1-2)

### Root (nivel 1)

- Pastas:
  - [.github/](../.github/)
  - [.vscode/](../.vscode/)
  - [archives/](../archives/)
  - [backup/](../backup/)
  - [BIBLIOTECA/](../BIBLIOTECA/)
  - [BIBLIOTECA_git_backup/](../BIBLIOTECA_git_backup/)
  - [data/](../data/)
  - [db/](../db/)
  - [docs/](../docs/)
  - [Documentaçao Auxiliar  Mundo Virtual Villa/](../Documenta%C3%A7ao%20Auxiliar%20%20Mundo%20Virtual%20Villa/)
  - [exports/](../exports/)
  - [GEMINI.md/](../GEMINI.md/)
  - [KLM localidade/](../KLM%20localidade/)
  - [out/](../out/)
  - [plans/](../plans/)
  - [reports/](../reports/)
  - [scripts/](../scripts/)
  - [Villa_Canabrava_Digital_World/](../Villa_Canabrava_Digital_World/)
  - [_kml_test/](../_kml_test/)
- Arquivos no root:
  - [.env](../.env)
  - [.env.example](../.env.example)
  - [.gitignore](../.gitignore)
  - [ADICIONAR_POSTGRESQL_PATH_WINDOWS.md](../ADICIONAR_POSTGRESQL_PATH_WINDOWS.md)
  - [ANALISE_CONSOLIDADA_REVISAO_COMPLETA_6FEB.md](../ANALISE_CONSOLIDADA_REVISAO_COMPLETA_6FEB.md)
  - [analyze_bounds.ps1](../analyze_bounds.ps1)
  - [BENCHMARKING_SETUP_REPORT_FEB7.md](../BENCHMARKING_SETUP_REPORT_FEB7.md)
  - [collect_baseline_metrics.py](../collect_baseline_metrics.py)
  - [collect_evidence.ps1](../collect_evidence.ps1)
  - [collect_opt1_metrics.py](../collect_opt1_metrics.py)
  - [collect_opt2_opt5_metrics_template.py](../collect_opt2_opt5_metrics_template.py)
  - [COMUNICACAO_FINAL_P0_FASE2.md](../COMUNICACAO_FINAL_P0_FASE2.md)
  - [CONCLUSAO_REVISAO_RECOMENDACOES_FINAIS.md](../CONCLUSAO_REVISAO_RECOMENDACOES_FINAIS.md)
  - [CONSOLIDATED_VALIDATION_REPORT_WEEK2_4.json](../CONSOLIDATED_VALIDATION_REPORT_WEEK2_4.json)
  - [CONTINUIDADE_PROJETO_EXECUCAO_HOJE_FEB6.md](../CONTINUIDADE_PROJETO_EXECUCAO_HOJE_FEB6.md)
  - [CREATIVE_P0_IMPROVEMENTS_FASE2.md](../CREATIVE_P0_IMPROVEMENTS_FASE2.md)
  - [DAILY_SYNC_01_FEB7_CONVOCACAO.md](../DAILY_SYNC_01_FEB7_CONVOCACAO.md)
  - [DB_VALIDATION_REPORT_POST_REMEDIATION.json](../DB_VALIDATION_REPORT_POST_REMEDIATION.json)
  - [docker-compose.yml](../docker-compose.yml)
  - [doc_generation_pipeline_v1.py](../doc_generation_pipeline_v1.py)
  - [ESTADO_ATUAL_SPRINT_2.md](../ESTADO_ATUAL_SPRINT_2.md)
  - [EVIDENCE_READY_CHECKLIST.md](../EVIDENCE_READY_CHECKLIST.md)
  - [EVIDENCIAS_PADRAO.md](../EVIDENCIAS_PADRAO.md)
  - [EXECUCAO_ATUALIZACAO_STATUS_SESSSAO_6FEB.md](../EXECUCAO_ATUALIZACAO_STATUS_SESSSAO_6FEB.md)
  - [EXECUCAO_PROJETO_STATUS_6FEB.md](../EXECUCAO_PROJETO_STATUS_6FEB.md)
  - [EXECUTOR_FUNCOES_FINALIZACAO.md](../EXECUTOR_FUNCOES_FINALIZACAO.md)
  - [gis_async_geometry_validator.py](../gis_async_geometry_validator.py)
  - [gis_async_pipeline_results_v2.json](../gis_async_pipeline_results_v2.json)
  - [gis_async_pipeline_validator_v2.env.example](../gis_async_pipeline_validator_v2.env.example)
  - [gis_async_pipeline_validator_v2.py](../gis_async_pipeline_validator_v2.py)
  - [GIS_BOUNDS_REPORT_P0_RECONCILIATION.md](../GIS_BOUNDS_REPORT_P0_RECONCILIATION.md)
  - [GO_LIVE_CHECKPOINTS_CRITERIA.md](../GO_LIVE_CHECKPOINTS_CRITERIA.md)
  - [grafana_dashboard_rastreabilidade_v1.json](../grafana_dashboard_rastreabilidade_v1.json)
  - [GUIA_TECNICO_PREFLIGHT_PATHS.md](../GUIA_TECNICO_PREFLIGHT_PATHS.md)
  - [HANDOFF_EXECUTOR_PARA_VALIDADOR.md](../HANDOFF_EXECUTOR_PARA_VALIDADOR.md)
  - [import_summary.json](../import_summary.json)
  - [INDEX_INFRAESTRUTURA_WEEK2_4.md](../INDEX_INFRAESTRUTURA_WEEK2_4.md)
  - [INDICE_EXECUCAO_PRODUCAO_SPRINT3.md](../INDICE_EXECUCAO_PRODUCAO_SPRINT3.md)
  - [INDICE_REVISAO_COMPLETA_6FEB.md](../INDICE_REVISAO_COMPLETA_6FEB.md)
  - [INSTALAR_POSTGRESQL_WINDOWS.md](../INSTALAR_POSTGRESQL_WINDOWS.md)
  - [KICKOFF_EXECUCAO_HOJE_6FEB.md](../KICKOFF_EXECUCAO_HOJE_6FEB.md)
  - [NOTIFICACAO_AGENT_DB_STAGE2_3_FEB6.md](../NOTIFICACAO_AGENT_DB_STAGE2_3_FEB6.md)
  - [NOTIFICACAO_CACHE_AGENT_STAGE2_3_FEB6.md](../NOTIFICACAO_CACHE_AGENT_STAGE2_3_FEB6.md)
  - [NOTIFICACAO_DOCS_AGENT_STAGE2_3_FEB6.md](../NOTIFICACAO_DOCS_AGENT_STAGE2_3_FEB6.md)
  - [NOTIFICACAO_EXECUTOR_ORQUESTRADOR_STAGE2_3_FEB6.md](../NOTIFICACAO_EXECUTOR_ORQUESTRADOR_STAGE2_3_FEB6.md)
  - [NOTIFICACAO_OBSERVABILITY_AGENT_STAGE2_3_FEB6.md](../NOTIFICACAO_OBSERVABILITY_AGENT_STAGE2_3_FEB6.md)
  - [NOTIFICACAO_TEAM_BROADCAST_STAGE2_3_COMPLETO_FEB6.md](../NOTIFICACAO_TEAM_BROADCAST_STAGE2_3_COMPLETO_FEB6.md)
  - [OPT1_DRYRUN_LOG.txt](../OPT1_DRYRUN_LOG.txt)
  - [OPT2_COLUMNAR_STORAGE_GIS_MIGRATION.sql](../OPT2_COLUMNAR_STORAGE_GIS_MIGRATION.sql)
  - [OPT2_COLUMNAR_STORAGE_VALIDATION_REPORT.json](../OPT2_COLUMNAR_STORAGE_VALIDATION_REPORT.json)
  - [OPT2_COLUMNAR_STORAGE_VALIDATOR.py](../OPT2_COLUMNAR_STORAGE_VALIDATOR.py)
  - [OPT2_OPT5_PERFORMANCE_SIMULATION_REPORT.json](../OPT2_OPT5_PERFORMANCE_SIMULATION_REPORT.json)
  - [OPT2_OPT5_PERFORMANCE_SIMULATOR.py](../OPT2_OPT5_PERFORMANCE_SIMULATOR.py)
  - [OPT3_INDEXED_VIEWS_RPC_SEARCH.sql](../OPT3_INDEXED_VIEWS_RPC_SEARCH.sql)
  - [OPT3_INDEXED_VIEWS_RPC_VALIDATION_REPORT.json](../OPT3_INDEXED_VIEWS_RPC_VALIDATION_REPORT.json)
  - [OPT3_INDEXED_VIEWS_VALIDATOR.py](../OPT3_INDEXED_VIEWS_VALIDATOR.py)
  - [OPT45_PARTITION_SCHEDULING_VALIDATION_REPORT.json](../OPT45_PARTITION_SCHEDULING_VALIDATION_REPORT.json)
  - [OPT45_PARTITION_SCHEDULING_VALIDATOR.py](../OPT45_PARTITION_SCHEDULING_VALIDATOR.py)
  - [OPT4_OPT5_PARTITION_SCHEDULING.sql](../OPT4_OPT5_PARTITION_SCHEDULING.sql)
  - [OPT_EXECUTION_PLAN_PARALELO_6FEB.md](../OPT_EXECUTION_PLAN_PARALELO_6FEB.md)
  - [ORQUESTRADOR_SPRINT_3_ARQUITETURA_AGENTES.md](../ORQUESTRADOR_SPRINT_3_ARQUITETURA_AGENTES.md)
  - [P0_CREATIVE_IMPROVEMENTS_FRAMEWORK.md](../P0_CREATIVE_IMPROVEMENTS_FRAMEWORK.md)
  - [P0_GOVERNANCA_CONSOLIDACAO_FINAL.md](../P0_GOVERNANCA_CONSOLIDACAO_FINAL.md)
  - [P0_REGISTRO_OFICIAL_FASE2_FECHAMENTO.md](../P0_REGISTRO_OFICIAL_FASE2_FECHAMENTO.md)
  - [PHASE_2_FINAL_CLOSURE_SIGNOFF_6FEB.md](../PHASE_2_FINAL_CLOSURE_SIGNOFF_6FEB.md)
  - [PLANO_ACAO_EXECUTIVO_6FEB_REVISADO.md](../PLANO_ACAO_EXECUTIVO_6FEB_REVISADO.md)
  - [POSTGRESQL_PORT_CONFIG.md](../POSTGRESQL_PORT_CONFIG.md)
  - [POST_DEPLOY_MONITORING_CHECKLIST.md](../POST_DEPLOY_MONITORING_CHECKLIST.md)
  - [POST_DEPLOY_STATUS_REPORT_FEB6.md](../POST_DEPLOY_STATUS_REPORT_FEB6.md)
  - [PREFLIGHT_VALIDATION_REPORT_6FEB.md](../PREFLIGHT_VALIDATION_REPORT_6FEB.md)
  - [PRODUCTION_DEPLOYMENT_OPT1_MON17.py](../PRODUCTION_DEPLOYMENT_OPT1_MON17.py)
  - [PRODUCTION_DEPLOY_PACKAGE_FEB6.md](../PRODUCTION_DEPLOY_PACKAGE_FEB6.md)
  - [PRODUCTION_PRE_CUTOVER_CHECKLIST.md](../PRODUCTION_PRE_CUTOVER_CHECKLIST.md)
  - [PROXIMA_FASE_KICKOFF_EXECUTIVO_FEB7.md](../PROXIMA_FASE_KICKOFF_EXECUTIVO_FEB7.md)
  - [PROXIMOS_PASSOS_ACAO_IMEDIATA.md](../PROXIMOS_PASSOS_ACAO_IMEDIATA.md)
  - [README_EXECUCAO.md](../README_EXECUCAO.md)
  - [redis_bounds_cache_config.sh](../redis_bounds_cache_config.sh)
  - [redis_ha_sentinel_circuit_breaker_v1.py](../redis_ha_sentinel_circuit_breaker_v1.py)
  - [REPORT_ESTADO_ATUAL.md](../REPORT_ESTADO_ATUAL.md)
  - [REPORT_ULTIMOS_25_COMANDOS.md](../REPORT_ULTIMOS_25_COMANDOS.md)
  - [requirements-gis.txt](../requirements-gis.txt)
  - [RESULTADO_EXECUCAO_INICIAL_FEB6.md](../RESULTADO_EXECUCAO_INICIAL_FEB6.md)
  - [ROADMAP_WEEK2_4_STAGING_PREP.md](../ROADMAP_WEEK2_4_STAGING_PREP.md)
  - [ROLLBACK_OPT1_temporal_partitioning_geometrias.sql](../ROLLBACK_OPT1_temporal_partitioning_geometrias.sql)
  - [ROLLBACK_OPT2_columnar_storage_gis.sql](../ROLLBACK_OPT2_columnar_storage_gis.sql)
  - [ROLLBACK_OPT3_indexed_views_rpc_search.sql](../ROLLBACK_OPT3_indexed_views_rpc_search.sql)
  - [ROLLBACK_OPT4_auto_partition_creation_2029_plus.sql](../ROLLBACK_OPT4_auto_partition_creation_2029_plus.sql)
  - [ROLLBACK_OPT5_mv_refresh_scheduling_cron.sql](../ROLLBACK_OPT5_mv_refresh_scheduling_cron.sql)
  - [ROLLOUT_PLAN_4WEEKS_FEB6.md](../ROLLOUT_PLAN_4WEEKS_FEB6.md)
  - [ROLLOUT_PLAN_4_SEMANAS.md](../ROLLOUT_PLAN_4_SEMANAS.md)
  - [RUNBOOK_OPT1_PRODUCTION_ROLLOUT.md](../RUNBOOK_OPT1_PRODUCTION_ROLLOUT.md)
  - [RUN_ALL_VALIDATORS_WEEK2_4.py](../RUN_ALL_VALIDATORS_WEEK2_4.py)
  - [run_preflight_validation.ps1](../run_preflight_validation.ps1)
  - [run_stage2_opt1_dryrun.ps1](../run_stage2_opt1_dryrun.ps1)
  - [run_stage4_executor.py](../run_stage4_executor.py)
  - [setup_benchmarking.py](../setup_benchmarking.py)
  - [setup_benchmarking_schema.sql](../setup_benchmarking_schema.sql)
  - [SPRINT3_EXECUCAO_COMPLETA_MESTRE.md](../SPRINT3_EXECUCAO_COMPLETA_MESTRE.md)
  - [SPRINT3_EXECUTOR_FINAL.py](../SPRINT3_EXECUTOR_FINAL.py)
  - [SPRINT3_EXECUTOR_WINDOWS_COMPATIBLE.py](../SPRINT3_EXECUTOR_WINDOWS_COMPATIBLE.py)
  - [SPRINT3_INDICE_COMPLETO.md](../SPRINT3_INDICE_COMPLETO.md)
  - [SPRINT3_KICKOFF_CEREMONY_OPT1_APPROVED.md](../SPRINT3_KICKOFF_CEREMONY_OPT1_APPROVED.md)
  - [SPRINT3_KICKOFF_EXECUCAO_HOJE_FEB6.md](../SPRINT3_KICKOFF_EXECUCAO_HOJE_FEB6.md)
  - [SPRINT3_OPT1_OPT5_CONSOLIDATION_REPORT.md](../SPRINT3_OPT1_OPT5_CONSOLIDATION_REPORT.md)
  - [SPRINT3_OPT1_VALIDATION_COMPLETE_FINAL.md](../SPRINT3_OPT1_VALIDATION_COMPLETE_FINAL.md)
  - [SPRINT3_RASTREABILIDADE_MASTER_ATUALIZADA.md](../SPRINT3_RASTREABILIDADE_MASTER_ATUALIZADA.md)
  - [SPRINT3_RESULTADO_EXECUCAO_FEB6.md](../SPRINT3_RESULTADO_EXECUCAO_FEB6.md)
  - [SPRINT3_RESUMO_EXECUTIVO_FEB6.md](../SPRINT3_RESUMO_EXECUTIVO_FEB6.md)
  - [SPRINT3_SHADOW_DEPLOYMENT_EXECUTOR.py](../SPRINT3_SHADOW_DEPLOYMENT_EXECUTOR.py)
  - [SPRINT3_SHADOW_DEPLOYMENT_PLAN_WEEK2.md](../SPRINT3_SHADOW_DEPLOYMENT_PLAN_WEEK2.md)
  - [SPRINT3_START_HERE_README.md](../SPRINT3_START_HERE_README.md)
  - [SPRINT3_VALIDADOR_METRICAS.py](../SPRINT3_VALIDADOR_METRICAS.py)
  - [SPRINT3_VALIDADOR_METRICAS_FIXED.py](../SPRINT3_VALIDADOR_METRICAS_FIXED.py)
  - [SPRINT_1_CONSOLIDACAO_FINAL.md](../SPRINT_1_CONSOLIDACAO_FINAL.md)
  - [SPRINT_2_ACTION_ITEMS.md](../SPRINT_2_ACTION_ITEMS.md)
  - [SPRINT_2_BACKLOG_PRIORIZADO.md](../SPRINT_2_BACKLOG_PRIORIZADO.md)
  - [SPRINT_2_CONSOLIDACAO_EXECUTIVA.md](../SPRINT_2_CONSOLIDACAO_EXECUTIVA.md)
  - [SPRINT_2_CONSOLIDACAO_FINAL.md](../SPRINT_2_CONSOLIDACAO_FINAL.md)
  - [SPRINT_2_DASHBOARD_EXECUTIVO.md](../SPRINT_2_DASHBOARD_EXECUTIVO.md)
  - [SPRINT_2_EXEC_REPORT.md](../SPRINT_2_EXEC_REPORT.md)
  - [SPRINT_2_FASE_3_KICKOFF.md](../SPRINT_2_FASE_3_KICKOFF.md)
  - [SPRINT_2_INDICE_DOCUMENTOS.md](../SPRINT_2_INDICE_DOCUMENTOS.md)
  - [SPRINT_2_KPIS.md](../SPRINT_2_KPIS.md)
  - [SPRINT_2_RESUMO_ORQUESTRADOR.md](../SPRINT_2_RESUMO_ORQUESTRADOR.md)
  - [SPRINT_2_STATUS_FINAL_PARA_VALIDADOR.md](../SPRINT_2_STATUS_FINAL_PARA_VALIDADOR.md)
  - [SPRINT_2_SUMARIO_METRICAS_FINAIS.md](../SPRINT_2_SUMARIO_METRICAS_FINAIS.md)
  - [SPRINT_2_TECH_OPTIMIZATIONS.md](../SPRINT_2_TECH_OPTIMIZATIONS.md)
  - [SPRINT_2_VALIDACAO_ARTEFATOS.md](../SPRINT_2_VALIDACAO_ARTEFATOS.md)
  - [SPRINT_3_CONSOLIDACAO_FINAL.md](../SPRINT_3_CONSOLIDACAO_FINAL.md)
  - [SPRINT_3_CONSOLIDACAO_SHADOW_VALIDATION.md](../SPRINT_3_CONSOLIDACAO_SHADOW_VALIDATION.md)
  - [SPRINT_3_DOCUMENTACAO_INDEX.md](../SPRINT_3_DOCUMENTACAO_INDEX.md)
  - [SPRINT_3_ESTADO_PRONTO_EXECUCAO.md](../SPRINT_3_ESTADO_PRONTO_EXECUCAO.md)
  - [SPRINT_3_EXECUTION_MASTER_PLAN_FEB6.md](../SPRINT_3_EXECUTION_MASTER_PLAN_FEB6.md)
  - [SPRINT_3_EXECUTOR_KICKOFF.md](../SPRINT_3_EXECUTOR_KICKOFF.md)
  - [SPRINT_3_EXEC_PROGRESS.md](../SPRINT_3_EXEC_PROGRESS.md)
  - [SPRINT_3_KPIS.md](../SPRINT_3_KPIS.md)
  - [SPRINT_3_OPT1_VALIDATION_HANDOFF.md](../SPRINT_3_OPT1_VALIDATION_HANDOFF.md)
  - [SPRINT_3_QUICKSTART_CHECKLIST.md](../SPRINT_3_QUICKSTART_CHECKLIST.md)
  - [SPRINT_3_README_INICIO_RAPIDO.md](../SPRINT_3_README_INICIO_RAPIDO.md)
  - [SPRINT_3_TEST_INTEGRATION.md](../SPRINT_3_TEST_INTEGRATION.md)
  - [stage2_opt1_dryrun_simple.py](../stage2_opt1_dryrun_simple.py)
  - [STAGE4_EXECUTOR_WINDOWS.py](../STAGE4_EXECUTOR_WINDOWS.py)
  - [STAGE4_FULL_SIMULATOR.py](../STAGE4_FULL_SIMULATOR.py)
  - [STAGE4_METRICS_COMPLETE_FEB6.json](../STAGE4_METRICS_COMPLETE_FEB6.json)
  - [STAGE4_NEXTGEN_EXECUTOR.py](../STAGE4_NEXTGEN_EXECUTOR.py)
  - [STAGE4_OPTIMIZATION_EXECUTOR.py](../STAGE4_OPTIMIZATION_EXECUTOR.py)
  - [stage_2_opt1_dryrun_validator.py](../stage_2_opt1_dryrun_validator.py)
  - [STAGING_DEPLOYMENT_SCRIPT_WEEK1.py](../STAGING_DEPLOYMENT_SCRIPT_WEEK1.py)
  - [STAGING_DEPLOY_SCRIPT_WEEK1.ps1](../STAGING_DEPLOY_SCRIPT_WEEK1.ps1)
  - [STAGING_TRANSITION_REPORT.md](../STAGING_TRANSITION_REPORT.md)
  - [STAGING_TRANSITION_REPORT_FEB6.md](../STAGING_TRANSITION_REPORT_FEB6.md)
  - [STARTUP_OPT_EXECUTION_DOCKER_LOCAL.md](../STARTUP_OPT_EXECUTION_DOCKER_LOCAL.md)
  - [STATUS_EXECUCAO_FINAL_WEEK2_4.md](../STATUS_EXECUCAO_FINAL_WEEK2_4.md)
  - [SUMARIO_EXECUCAO_SPRINT3_COMPLETO.md](../SUMARIO_EXECUCAO_SPRINT3_COMPLETO.md)
  - [SUMARIO_EXECUCAO_WEEK2_4_INFRASTRUCTURE.md](../SUMARIO_EXECUCAO_WEEK2_4_INFRASTRUCTURE.md)
  - [SUMARIO_EXECUTIVO_1_PAGINA.md](../SUMARIO_EXECUTIVO_1_PAGINA.md)
  - [SUPABASE_CREDENTIALS_TEMPLATE.env](../SUPABASE_CREDENTIALS_TEMPLATE.env)
  - [TIMELINE_EXECUTIVA_PRODUCAO.md](../TIMELINE_EXECUTIVA_PRODUCAO.md)
  - [TIMING_VALIDATORS_EXECUTION.md](../TIMING_VALIDATORS_EXECUTION.md)
  - [validate-gis.ps1](../validate-gis.ps1)
  - [validate_opt1_feb7.ps1](../validate_opt1_feb7.ps1)
  - [validate_sprint2_migrations.ps1](../validate_sprint2_migrations.ps1)
  - [validate_sprint2_migrations_simple.py](../validate_sprint2_migrations_simple.py)
  - [validation_report.md](../validation_report.md)
  - [VALIDATION_REPORT_P0_FINAL.md](../VALIDATION_REPORT_P0_FINAL.md)
  - [VALIDATION_REPORT_SPRINT_1.md](../VALIDATION_REPORT_SPRINT_1.md)
  - [VALIDATION_REPORT_SPRINT_2.md](../VALIDATION_REPORT_SPRINT_2.md)

### .github/ (nivel 2)

- [workflows/](../.github/workflows/)
  - [p0-preflight-checks.yml](../.github/workflows/p0-preflight-checks.yml)

### .vscode/ (nivel 2)

- [settings.json](../.vscode/settings.json)

### archives/ (nivel 2)

- [2026-02-07/](../archives/2026-02-07/)
  - [backups_raw/](../archives/2026-02-07/backups_raw/)
  - [legacy_projects/](../archives/2026-02-07/legacy_projects/)
  - [logs/](../archives/2026-02-07/logs/)
  - [metrics/](../archives/2026-02-07/metrics/)
  - [shadow/](../archives/2026-02-07/shadow/)
  - [venv/](../archives/2026-02-07/venv/)
  - [zips/](../archives/2026-02-07/zips/)

### backup/ (nivel 2)

- [geometrias.dump](../backup/geometrias.dump)

### BIBLIOTECA/ (nivel 2)

- [.browser_screenshots/](../BIBLIOTECA/.browser_screenshots/)
- [.gitignore](../BIBLIOTECA/.gitignore)
- [.venv/](../BIBLIOTECA/.venv/)
- [.vercel/](../BIBLIOTECA/.vercel/)
- [.vscode/](../BIBLIOTECA/.vscode/)
- [ANALISE_DETALHADA_PROJETO_COMPLETO.md](../BIBLIOTECA/ANALISE_DETALHADA_PROJETO_COMPLETO.md)
- [assets/](../BIBLIOTECA/assets/)
- [AUDITORIA_EXTERNA_COMPLETA_PARECER_FINAL.md](../BIBLIOTECA/AUDITORIA_EXTERNA_COMPLETA_PARECER_FINAL.md)
- [AUTOPSIA_ESTADO_ATUAL_6FEB_COMPLETA.md](../BIBLIOTECA/AUTOPSIA_ESTADO_ATUAL_6FEB_COMPLETA.md)
- [BLOQUEADORES_PRE_SEMANA_2.md](../BIBLIOTECA/BLOQUEADORES_PRE_SEMANA_2.md)
- [CONCLUSAO_EXECUCAO_6FEB_RESUMO_FINAL.md](../BIBLIOTECA/CONCLUSAO_EXECUCAO_6FEB_RESUMO_FINAL.md)
- [CONFIRMACAO_ESTRUTURA_PRONTA.md](../BIBLIOTECA/CONFIRMACAO_ESTRUTURA_PRONTA.md)
- [CONFORMIDADE_POS_AUDITORIA_6FEB.md](../BIBLIOTECA/CONFORMIDADE_POS_AUDITORIA_6FEB.md)
- [CORRECOES_INCONSISTENCIAS_DOCUMENTAIS.md](../BIBLIOTECA/CORRECOES_INCONSISTENCIAS_DOCUMENTAIS.md)
- [DIAGNOSTICO_9_PROBLEMAS_CRITICOS.md](../BIBLIOTECA/DIAGNOSTICO_9_PROBLEMAS_CRITICOS.md)
- [DIAGNOSTICO_CORRECOES_6FEB_RELATORIO_FINAL.md](../BIBLIOTECA/DIAGNOSTICO_CORRECOES_6FEB_RELATORIO_FINAL.md)
- [DOCKER_SUPABASE_SETUP.md](../BIBLIOTECA/DOCKER_SUPABASE_SETUP.md)
- [docs/](../BIBLIOTECA/docs/)
- [ESTADO_DE_VERDADE_UNICO_6FEB.md](../BIBLIOTECA/ESTADO_DE_VERDADE_UNICO_6FEB.md)
- [EXECUCAO_FEEDBACK_AUDITOR_6FEB_FINAL.md](../BIBLIOTECA/EXECUCAO_FEEDBACK_AUDITOR_6FEB_FINAL.md)
- [FASE_1_READY_FOR_EXECUTION.md](../BIBLIOTECA/FASE_1_READY_FOR_EXECUTION.md)
- [FASE_2_ESTRUTURA_ORGANIZADA.md](../BIBLIOTECA/FASE_2_ESTRUTURA_ORGANIZADA.md)
- [FASE_2_ESTRUTURA_PRONTA.md](../BIBLIOTECA/FASE_2_ESTRUTURA_PRONTA.md)
- [FASE_2_INDICE_EXECUCAO.md](../BIBLIOTECA/FASE_2_INDICE_EXECUCAO.md)
- [FASE_2_QUICKSTART_CHECKLIST.md](../BIBLIOTECA/FASE_2_QUICKSTART_CHECKLIST.md)
- [FASE_2_READY_FOR_EXECUTION.md](../BIBLIOTECA/FASE_2_READY_FOR_EXECUTION.md)
- [FASE_2_SEMANAS_2_3_4_TRACKING.md](../BIBLIOTECA/FASE_2_SEMANAS_2_3_4_TRACKING.md)
- [FINALIZACAO_AUDITORIA_6FEB_PRONTO_PUSH.md](../BIBLIOTECA/FINALIZACAO_AUDITORIA_6FEB_PRONTO_PUSH.md)
- [FRAMEWORK_CONTINUIDADE_PROCEDIMENTOS.md](../BIBLIOTECA/FRAMEWORK_CONTINUIDADE_PROCEDIMENTOS.md)
- [frontend/](../BIBLIOTECA/frontend/)
- [GOVERNANCE_POLITICA_OPERACOES.md](../BIBLIOTECA/GOVERNANCE_POLITICA_OPERACOES.md)
- [INDICE_DEVOPS_VILLA_CANABRAVA.md](../BIBLIOTECA/INDICE_DEVOPS_VILLA_CANABRAVA.md)
- [INDICE_EXECUTIVO_ANALISE_DETALHADA.md](../BIBLIOTECA/INDICE_EXECUTIVO_ANALISE_DETALHADA.md)
- [INSTRUCOES_REVALIDACAO_SEMANA_2.md](../BIBLIOTECA/INSTRUCOES_REVALIDACAO_SEMANA_2.md)
- [MANIFESTO_METODOLOGIA_CONTINUIDADE.md](../BIBLIOTECA/MANIFESTO_METODOLOGIA_CONTINUIDADE.md)
- [PARECER_AUDITORIA_FINAL_NAO_APROVADO_6FEB.md](../BIBLIOTECA/PARECER_AUDITORIA_FINAL_NAO_APROVADO_6FEB.md)
- [pasra_site/](../BIBLIOTECA/pasra_site/)
- [PLANO_ESTRATEGICO_CONSOLIDADO_S2_6FEB.md](../BIBLIOTECA/PLANO_ESTRATEGICO_CONSOLIDADO_S2_6FEB.md)
- [PLANO_EXECUCAO_IMEDIATA_AGENTE_OPERACOES.md](../BIBLIOTECA/PLANO_EXECUCAO_IMEDIATA_AGENTE_OPERACOES.md)
- [PLANO_EXECUCAO_SEMANA_2_DETALHADO.md](../BIBLIOTECA/PLANO_EXECUCAO_SEMANA_2_DETALHADO.md)
- [plans/](../BIBLIOTECA/plans/)
- [project_analysis/](../BIBLIOTECA/project_analysis/)
- [PROMPT_EXECUCAO_FASE_1.md](../BIBLIOTECA/PROMPT_EXECUCAO_FASE_1.md)
- [PROMPT_EXECUCAO_FASE_2.md](../BIBLIOTECA/PROMPT_EXECUCAO_FASE_2.md)
- [PROMPT_EXECUCAO_SEMANAS_2_3_4_FASE_2.md](../BIBLIOTECA/PROMPT_EXECUCAO_SEMANAS_2_3_4_FASE_2.md)
- [PROMPT_VALIDACAO_FASE_0.md](../BIBLIOTECA/PROMPT_VALIDACAO_FASE_0.md)
- [PROMPT_VALIDACAO_FASE_1.md](../BIBLIOTECA/PROMPT_VALIDACAO_FASE_1.md)
- [PROMPT_VALIDACAO_FASE_2.md](../BIBLIOTECA/PROMPT_VALIDACAO_FASE_2.md)
- [README.md](../BIBLIOTECA/README.md)
- [RELATORIO_AUTOPSIA_DEVOPS_VILLA_CANABRAVA.md](../BIBLIOTECA/RELATORIO_AUTOPSIA_DEVOPS_VILLA_CANABRAVA.md)
- [RELATORIO_CORRECOES_APLICADAS.md](../BIBLIOTECA/RELATORIO_CORRECOES_APLICADAS.md)
- [RELATORIO_CORRECOES_SEMANA_1_FASE_2.md](../BIBLIOTECA/RELATORIO_CORRECOES_SEMANA_1_FASE_2.md)
- [RELATORIO_ESTRUTURACAO_SEMANAS_2_3_4.md](../BIBLIOTECA/RELATORIO_ESTRUTURACAO_SEMANAS_2_3_4.md)
- [RELATORIO_EXECUCAO_FASE_1.md](../BIBLIOTECA/RELATORIO_EXECUCAO_FASE_1.md)
- [RELATORIO_EXECUCAO_RODADA_6FEB_PARA_NOVA_VISTORIA.md](../BIBLIOTECA/RELATORIO_EXECUCAO_RODADA_6FEB_PARA_NOVA_VISTORIA.md)
- [REMEDIACAO_FINAL_AUDITORIA_6FEB_RESUMO.md](../BIBLIOTECA/REMEDIACAO_FINAL_AUDITORIA_6FEB_RESUMO.md)
- [REMEDIATION_APLICADA_FASE_1.md](../BIBLIOTECA/REMEDIATION_APLICADA_FASE_1.md)
- [REMEDIATION_SEMANA_2_FASE_2.md](../BIBLIOTECA/REMEDIATION_SEMANA_2_FASE_2.md)
- [reports/](../BIBLIOTECA/reports/)
- [requirements-gis.txt](../BIBLIOTECA/requirements-gis.txt)
- [RESPOSTA_AUDITOR_FINAL_6FEB.md](../BIBLIOTECA/RESPOSTA_AUDITOR_FINAL_6FEB.md)
- [REVISAO_CRITICA_ANALISE.md](../BIBLIOTECA/REVISAO_CRITICA_ANALISE.md)
- [ROADMAP_CAPACIDADES_S2_S4.md](../BIBLIOTECA/ROADMAP_CAPACIDADES_S2_S4.md)
- [RUNBOOK_DEVOPS_VILLA_CANABRAVA.md](../BIBLIOTECA/RUNBOOK_DEVOPS_VILLA_CANABRAVA.md)
- [S2_KICKOFF_CHECKLIST_FINAL.md](../BIBLIOTECA/S2_KICKOFF_CHECKLIST_FINAL.md)
- [SEMANA_1_FASE_2_RESUMO_FINAL.md](../BIBLIOTECA/SEMANA_1_FASE_2_RESUMO_FINAL.md)
- [SEMANA_2_COMECA_SEGUNDA.md](../BIBLIOTECA/SEMANA_2_COMECA_SEGUNDA.md)
- [SEMANA_2_KICKOFF_READINESS.md](../BIBLIOTECA/SEMANA_2_KICKOFF_READINESS.md)
- [STATUS_CRITICO_6FEB_CORRECOES_APLICADAS.md](../BIBLIOTECA/STATUS_CRITICO_6FEB_CORRECOES_APLICADAS.md)
- [SUMARIO_EXECUTIVO_DEVOPS_VILLA_CANABRAVA.md](../BIBLIOTECA/SUMARIO_EXECUTIVO_DEVOPS_VILLA_CANABRAVA.md)
- [supabase/](../BIBLIOTECA/supabase/)
- [tools/](../BIBLIOTECA/tools/)
- [TRANSICAO_ANALYSIS_EXECUTION_6FEB.md](../BIBLIOTECA/TRANSICAO_ANALYSIS_EXECUTION_6FEB.md)
- [user_input_files/](../BIBLIOTECA/user_input_files/)
- [VALIDACAO_DOCKER_SUPABASE_PASSO_A_PASSO.md](../BIBLIOTECA/VALIDACAO_DOCKER_SUPABASE_PASSO_A_PASSO.md)
- [VALIDACAO_SEMANA_1_FASE_2.md](../BIBLIOTECA/VALIDACAO_SEMANA_1_FASE_2.md)
- [VALIDACAO_SUPABASE_LOCAL_6FEB.md](../BIBLIOTECA/VALIDACAO_SUPABASE_LOCAL_6FEB.md)
- [vercel.json](../BIBLIOTECA/vercel.json)

### BIBLIOTECA_git_backup/ (nivel 2)

- Pasta vazia.

### data/ (nivel 2)

- [contract/](../data/contract/)
  - [villa_canabrava_contract.json](../data/contract/villa_canabrava_contract.json)
- [exports/](../data/exports/)
- [processed/](../data/processed/)
- [raw/](../data/raw/)
- [samples/](../data/samples/)

### db/ (nivel 2)

- [migrations/](../db/migrations/)
  - [0001_init.sql](../db/migrations/0001_init.sql)
  - [0002_idempotency.sql](../db/migrations/0002_idempotency.sql)
  - [0003_gis_data.sql](../db/migrations/0003_gis_data.sql)

### docs/ (nivel 2)

- [ENV.md](../docs/ENV.md)
- [INDEX.md](../docs/INDEX.md)
- [START_HERE.md](../docs/START_HERE.md)

### Documentaçao Auxiliar  Mundo Virtual Villa/ (nivel 2)

- [00_DOCUMENTACAO_OFICIAL_V2/](../Documenta%C3%A7ao%20Auxiliar%20%20Mundo%20Virtual%20Villa/00_DOCUMENTACAO_OFICIAL_V2/)
- [agents/](../Documenta%C3%A7ao%20Auxiliar%20%20Mundo%20Virtual%20Villa/agents/)
- [APLICATIVO-BIBLIOTECA-RC/](../Documenta%C3%A7ao%20Auxiliar%20%20Mundo%20Virtual%20Villa/APLICATIVO-BIBLIOTECA-RC/)

### exports/ (nivel 2)

- [geojson/](../exports/geojson/)

### GEMINI.md/ (nivel 2)

- [GEMINI.md](../GEMINI.md/GEMINI.md)

### KLM localidade/ (nivel 2)

- Pasta vazia.

### out/ (nivel 2)

- [golden/](../out/golden/)
  - 252 arquivos .geojson + [manifest.json](../out/golden/manifest.json).
- [reports/](../out/reports/)
  - [export_report.md](../out/reports/export_report.md)
  - [validation_report.md](../out/reports/validation_report.md)

### plans/ (nivel 2)

- [P0_CHECKLIST_VALIDACAO.md](../plans/P0_CHECKLIST_VALIDACAO.md)
- [P0_VALIDATION_PLAN.md](../plans/P0_VALIDATION_PLAN.md)
- [SPRINT_2_PLANO_ORQUESTRADOR_FINAL.md](../plans/SPRINT_2_PLANO_ORQUESTRADOR_FINAL.md)
- [SPRINT_3_COMMUNICATION_LOG.md](../plans/SPRINT_3_COMMUNICATION_LOG.md)
- [SPRINT_3_PLANO_EXECUTIVO_FEB6_10.md](../plans/SPRINT_3_PLANO_EXECUTIVO_FEB6_10.md)
- [SPRINT_3_RASTREABILIDADE_MASTER.md](../plans/SPRINT_3_RASTREABILIDADE_MASTER.md)
- [SPRINT_3_RISK_REGISTER.md](../plans/SPRINT_3_RISK_REGISTER.md)

### reports/ (nivel 2)

- [00_env_audit.md](../reports/00_env_audit.md)
- [00_repo_duplicates.csv](../reports/00_repo_duplicates.csv)
- [00_repo_ext_counts.csv](../reports/00_repo_ext_counts.csv)
- [00_repo_inventory.md](../reports/00_repo_inventory.md)
- [00_repo_inventory_raw.txt](../reports/00_repo_inventory_raw.txt)
- [00_repo_top_dirs.csv](../reports/00_repo_top_dirs.csv)
- [00_repo_top_files.csv](../reports/00_repo_top_files.csv)
- [01_cleanup_plan.md](../reports/01_cleanup_plan.md)
- [01_schema_contract.md](../reports/01_schema_contract.md)
- [02_import_idempotency.md](../reports/02_import_idempotency.md)
- [02_reference_map.md](../reports/02_reference_map.md)
- [03_moves_executed.md](../reports/03_moves_executed.md)
- [03_spatial_quality.md](../reports/03_spatial_quality.md)
- [04_deletion_candidates.md](../reports/04_deletion_candidates.md)
- [04_metrics_vs_docs.md](../reports/04_metrics_vs_docs.md)
- [05_export.md](../reports/05_export.md)
- [99_fix_plan.md](../reports/99_fix_plan.md)
- [cleanup_run.log](../reports/cleanup_run.log)
- [import_report.csv](../reports/import_report.csv)
- [RELATORIO_CENARIO_ATUAL.md](../reports/RELATORIO_CENARIO_ATUAL.md)
- [RELATORIO_COMANDOS_PARA_EXECUCAO.md](../reports/RELATORIO_COMANDOS_PARA_EXECUCAO.md)
- [RELATORIO_ESTADO_ATUAL_E_LACUNAS.md](../reports/RELATORIO_ESTADO_ATUAL_E_LACUNAS.md)
- [skipped_report.csv](../reports/skipped_report.csv)

### scripts/ (nivel 2)

- [gis/](../scripts/gis/)
  - [export_geojson_from_postgis.py](../scripts/gis/export_geojson_from_postgis.py)
  - [import_kml_to_postgis.py](../scripts/gis/import_kml_to_postgis.py)
  - [run_pipeline.ps1](../scripts/gis/run_pipeline.ps1)
  - [validate_db.py](../scripts/gis/validate_db.py)
  - [validate_pipeline.py](../scripts/gis/validate_pipeline.py)
  - [__pycache__/](../scripts/gis/__pycache__/)
- [repo_cleanup.ps1](../scripts/repo_cleanup.ps1)
- [run_pipeline.ps1](../scripts/run_pipeline.ps1)

### Villa_Canabrava_Digital_World/ (nivel 2)

- [.venv/](../Villa_Canabrava_Digital_World/.venv/)
- [data/](../Villa_Canabrava_Digital_World/data/)
- [scripts/](../Villa_Canabrava_Digital_World/scripts/)

### _kml_test/ (nivel 2)

- [Perimetro.kml](../_kml_test/Perimetro.kml)

## Inventario e evidencias

- Inventario: [reports/00_repo_inventory.md](00_repo_inventory.md).
- Plano de limpeza: [reports/01_cleanup_plan.md](01_cleanup_plan.md).
- Movimentos executados: [reports/03_moves_executed.md](03_moves_executed.md).
- Log de limpeza: [reports/cleanup_run.log](cleanup_run.log).
- Indice geral: [docs/INDEX.md](../docs/INDEX.md).

## Estado recente da execucao

- O pipeline foi executado e as migracoes rodaram com sucesso.
- Houve falha inicial por dependencia Python (fiona) ausente; o pipeline foi ajustado para instalar dependencias automaticamente.
- O container PostGIS sobe com healthcheck e permanece em execucao.

## Riscos e pendencias

- A revisao do inventario mostra caminhos repetidos em archives/2026-02-07/ (necessita normalizacao em uma etapa futura).
- Subprojetos legados ainda estao no root e exigem decisao de arquivamento.
- Confirmar se o pipeline gera 252 layers e se o manifest esta em PASS.

## Como rodar o pipeline (1 comando)

```powershell
copy .env.example .env
.\scripts\run_pipeline.ps1 -KmlDir "C:\Users\rober\Downloads\KML\KML" -OutDir "out"
```

Com reset explicito:

```powershell
.\scripts\run_pipeline.ps1 -KmlDir "C:\Users\rober\Downloads\KML\KML" -OutDir "out" -Reset
```

## Onde ficam os resultados

- Golden GeoJSON: out/golden/
- Manifest: out/golden/manifest.json
- Report: out/reports/validation_report.md
