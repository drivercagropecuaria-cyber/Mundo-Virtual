# Variaveis de ambiente

Este projeto usa duas familias de variaveis:

## 1) Docker Compose (Postgres/PostGIS)

- POSTGRES_USER
- POSTGRES_PASSWORD
- POSTGRES_DB
- POSTGRES_PORT

Essas variaveis configuram o container Postgres.

## 2) Scripts Python (importacao e validacao)

- DB_HOST
- DB_PORT
- DB_NAME
- DB_USER
- DB_PASSWORD

Essas variaveis sao lidas pelos scripts em `scripts/` para conectar no banco.

## Exemplo de .env

```text
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=villa_canabrava
POSTGRES_PORT=15433
DB_HOST=localhost
DB_PORT=15433
DB_NAME=villa_canabrava
DB_USER=postgres
DB_PASSWORD=postgres
```

## Observacoes

- Para evitar conflito com outros bancos, use a porta 15433.
- Os scripts tambem aceitam `--db-url` para conectar sem usar variaveis.
