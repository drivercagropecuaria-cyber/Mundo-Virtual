# Relatorio de estado atual e lacunas

Data: 2026-02-07

## Estado atual

- Inventario consolidado em [00_repo_inventory.md](00_repo_inventory.md) com evidencias CSV.
- Plano de limpeza definido em [01_cleanup_plan.md](01_cleanup_plan.md).
- Scripts GIS canonicos em [../scripts/gis/](../scripts/gis/).
- Entrada canonica definida em [../docs/START_HERE.md](../docs/START_HERE.md) e indice em [../docs/INDEX.md](../docs/INDEX.md).
- Mapa de referencias criado em [02_reference_map.md](02_reference_map.md).
- Simulacao de limpeza executada (WhatIf) com log em [cleanup_run.log](cleanup_run.log).
- Cleanup executado com -ExcludeLegacy, arquivando ruido em archives/2026-02-07/.
- Referencias atualizadas para caminhos arquivados (com base no cleanup_run.log).

## Lacunas e riscos

- Cleanup executado em modo real, mantendo legados fora do archive.
- Root com menos ruido apos o archive; revisar arquivos restantes para segunda passada.
- Validacao compileall executada com Python do sistema (ver reports/RELATORIO_COMANDOS_PARA_EXECUCAO.md).
- Duplicatas e snapshots (zips e backups) ainda coexistem com fontes.
- Exportacoes GIS existem em exports/geojson e data/exports; falta consolidacao.
- Muitas referencias a caminhos legados (BIBLIOTECA e Villa_Canabrava_Digital_World) exigem revisao se houver movimentacao.

## Pendencias imediatas

- Revisar logs em [cleanup_run.log](cleanup_run.log) e confirmar exclusao de legados.
- Consolidar exports/geojson para data/exports/geojson (fase 2).
- Revisar subprojetos legados antes de arquivar (BIBLIOTECA_git_backup e Villa_Canabrava_Digital_World).
- Manter Python do sistema configurado, ou reavaliar venv local se necessario.
