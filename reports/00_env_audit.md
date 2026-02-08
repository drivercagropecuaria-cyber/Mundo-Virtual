# Relatorio de auditoria do ambiente (canonic)

Data: 2026-02-07

## Comandos executados

```powershell
$containers = docker ps --format "{{.Names}}\t{{.Image}}\t{{.Status}}\t{{.Ports}}"
$containers
"---"
$canon = "villa_canabrava_postgis"
if ($containers -match $canon) {
  docker inspect $canon --format "Mounts={{json .Mounts}}"
  "---"
  docker exec -i $canon psql -U postgres -d villa_canabrava -P pager=off -c "SELECT version();"
  docker exec -i $canon psql -U postgres -d villa_canabrava -P pager=off -c "SELECT PostGIS_Version();"
  docker exec -i $canon psql -U postgres -d villa_canabrava -P pager=off -c "\dn"
} else {
  "Container canonico nao encontrado: $canon"
}
```

## Saida coletada

```text
villa_canabrava_postgis postgis/postgis:15-3.3-alpine   Up 47 minutes (healthy) 0.0.0.0:15433->5432/tcp, [::]:15433->5432/tcp
postgres_test   postgis/postgis:15-3.3-alpine   Up 2 hours      127.0.0.1:15432->5432/tcp
---
Mounts=[{"Type":"volume","Name":"mundovirtualvillacanabrava_villa_canabrava_pgdata","Source":"/var/lib/docker/volumes/mundovirtualvillacanabrava_villa_canabrava_pgdata/_data","Destination":"/var/lib/postgresql/data","Driver":"local","Mode":"rw","RW":true,"Propagation":""}]
---
PostgreSQL 15.4 on x86_64-pc-linux-musl, compiled by gcc (Alpine 12.2.1_git20220924-r10) 12.2.1 20220924, 64-bit
(1 row)

postgis_version
---------------------------------------
3.3 USE_GEOS=1 USE_PROJ=1 USE_STATS=1
(1 row)

List of schemas
Name             | Owner
-----------------+-------------------
public           | pg_database_owner
tiger            | postgres
tiger_data       | postgres
topology         | postgres
villa_canabrava  | postgres
(5 rows)
```

## Conclusoes

- O container canonico esta ativo e saudavel: `villa_canabrava_postgis`.
- Postgres 15.4 e PostGIS 3.3 estao ativos.
- Schema `villa_canabrava` existe.
- Porta atual publicada: 15433.
- Existe outro container `postgres_test` na porta 15432.
