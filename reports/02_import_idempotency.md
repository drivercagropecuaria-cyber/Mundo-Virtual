# Relatorio de idempotencia da importacao

## Objetivo
Garantir que rodar o importador duas vezes gere o mesmo resultado.

## Estrategia aplicada

- Chave unica por arquivo: `source_kml + layer_name + feature_hash`.
- `feature_hash` e calculado a partir de nome, layer, geometria e atributos.
- Importacao pode limpar linhas do arquivo antes de inserir (por arquivo).

## Mudancas implementadas

- Novo arquivo de migracao: `db/migrations/0002_idempotency.sql`.
- Importador calcula `feature_hash` e usa `ON CONFLICT`.
- Opcao `--replace-existing` (padrao) remove dados do mesmo arquivo antes de inserir.

## Aplicacao da migracao (quando desejado)

```powershell
docker exec -i villa_canabrava_postgis psql -U postgres -d villa_canabrava -f db/migrations/0002_idempotency.sql
```

## Observacoes

- Linhas antigas nao possuem `feature_hash` e podem ser duplicadas se a chave unica ainda nao estiver aplicada.
- Para normalizar, aplique a migracao e rode um import completo com `--replace-existing`.
