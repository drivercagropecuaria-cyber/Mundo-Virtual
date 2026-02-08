# EVIDENCE READY - CHECKLIST AUTOMATICO

Objetivo: verificar se todos os artefatos do escopo fechado estao citados no EXEC_REPORT.

## Checklist (Sprint 1)
- [ ] EXEC_REPORT Sprint 1 presente e atualizado
- [ ] Pre-Flight log citado
- [ ] run_preflight_validation.ps1 citado
- [ ] GIS_BOUNDS_REPORT_P0_RECONCILIATION.md citado
- [ ] Logs/outputs de RPCs citados
- [ ] DB_VALIDATION_REPORT_POST_REMEDIATION.json citado (uso exclusivo para geometria)
- [ ] 1770369200_fix_all_views_catalogo_rename.sql citado
- [ ] 1770201200_update_catalogo_view_proxy.sql citado
- [ ] 1770169200_optimize_search_catalogo.sql citado
- [ ] gis_async_geometry_validator.py citado
- [ ] Timestamp atualizado

## Observacoes obrigatorias
- Se algum artefato do escopo estiver fora do EXEC_REPORT, bloquear validacao.
- Se o EXEC_REPORT nao incluir outputs executaveis (logs/commands), marcar como pendencia.
- Se houver risco recorrente de reprova por falta de provas, exigir bloco EVIDENCIAS PADRAO.
