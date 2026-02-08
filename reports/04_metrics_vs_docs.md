# Metricas vs documentacao

Data: 2026-02-07

## Tabela comparativa

| metrica | doc | calculada (banco) | diferenca | hipotese/causa | correcao sugerida |
| --- | --- | --- | --- | --- | --- |
| Total de features | nao informado | 665 | n/a | Importacoes acumuladas | Aplicar idempotencia e reimportar se necessario |
| Total de layers | nao informado | 250 | n/a | Nomes derivados por arquivo | Revisar padrao de nomes se houver duplicidade |
| Area perimetro (ha) | nao informado | 7729.257184 | n/a | Base atual possui 2 imports | Limpar duplicadas e recalcular |
| Area APP (ha) | nao informado | 85.433097 | n/a | Uniao por AREA_DE_APP% | Validar se camadas APP sao completas |
| Area RL (ha) | nao informado | 1550.302070 | n/a | Uniao por RL_% | Validar se todas RL estao no dataset |

## Metodologia de calculo

- Areas calculadas com uniao geometrica: `ST_UnaryUnion(ST_Collect(geometry))`.
- Conversao para hectares: `ST_Area(geography) / 10000`.
- Evita inflacao por sobreposicao.
