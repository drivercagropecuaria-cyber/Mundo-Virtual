# STAGE 4 - LOCAL ENV SETUP LOG (FEB 6)
## Environment: postgres_test / biblioteca

**Date:** 2026-02-06

---

## Commands Executed
1. Check database exists
```
docker exec postgres_test psql -U postgres -tAc "SELECT 1 FROM pg_database WHERE datname='BIBLIOTECA';"
```
**Result:** no output (DB missing)

2. Create database
```
docker exec postgres_test psql -U postgres -c "CREATE DATABASE BIBLIOTECA;"
```
**Result:** CREATE DATABASE

3. Check benchmarking schema
```
docker exec postgres_test psql -U postgres -d biblioteca -tAc "SELECT 1 FROM information_schema.schemata WHERE schema_name='benchmarking';"
```
**Result:** no output (schema missing)

4. Create benchmarking schema
```
Get-Content setup_benchmarking_schema.sql | docker exec -i postgres_test psql -U postgres -d biblioteca
```
**Result:** CREATE SCHEMA, tables, indexes, views

5. List benchmarking tables
```
docker exec postgres_test psql -U postgres -d biblioteca -c "SELECT table_name FROM information_schema.tables WHERE table_schema='benchmarking' ORDER BY table_name;"
```
**Result:** metrics_collection, query_execution_log, system_stats, vw_metrics_by_optimization, vw_query_execution_summary

6. Check geometrias table
```
docker exec postgres_test psql -U postgres -d biblioteca -tAc "SELECT 1 FROM information_schema.tables WHERE table_schema='public' AND table_name='geometrias';"
```
**Result:** no output (table missing)

---

## Outcome
- Database created
- Benchmarking schema created
- Benchmarking tables present
- Application data missing (geometrias)
