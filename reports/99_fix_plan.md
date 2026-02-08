# Plano de correcao final

## Ordem de execucao

1) Aplicar migracao de idempotencia (`db/migrations/0002_idempotency.sql`).
2) Rodar importacao completa com `--replace-existing`.
3) Rodar validacao (`scripts/gis/validate_db.py`).
4) Revisar `reports/skipped_report.csv` e tratar falhas recorrentes.
5) Exportar GeoJSON por camada.

## Riscos

- Duplicacao de dados se importar sem `--replace-existing`.
- Inconsistencias de area se camadas sobrepostas nao forem unificadas.
- Vazamento de porta se Postgres nao estiver preso em 127.0.0.1.

## Rollback

- Backup previo com `pg_dump`.
- Restauracao com `pg_restore` se houver perda de dados.
- Manter copia de `reports/` e `exports/` para auditoria.

## Checklist final: PRONTO PARA O MUNDO VIRTUAL

- [ ] Container PostGIS canonico ativo na porta 15433.
- [ ] Schema `villa_canabrava` com migracoes aplicadas.
- [ ] Importacao idempotente executada com sucesso.
- [ ] Validacao PASS em `validation_report.md`.
- [ ] `reports/skipped_report.csv` revisado.
- [ ] Exportacao GeoJSON concluida.
