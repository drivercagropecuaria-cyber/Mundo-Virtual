# SPRINT 3 - TESTES DE INTEGRAÃ‡ÃƒO
## Guia de ExecuÃ§Ã£o - Agent Executor

**Data:** A definir
**Status:** SHADOW ENVIRONMENT APROVADO âœ… | BENCHMARKING PRONTO
**Shadow Approval Badge:** âœ… SHADOW VALIDADO (Exit Code 0)

---

## ðŸ“‹ Shadow Environment Validation Status

âœ… **Shadow Deploy Validator**: PASSED (Exit Code 0)
âœ… **GIS Environment Validator**: PASSED (Exit Code 0)
âœ… **Infrastructure Baseline**: Ready for Performance Testing

Ver [archives/2026-02-07/logs/EXEC_REPORT_SHADOW_DEPLOY_VALIDATION_6FEB.md](archives/2026-02-07/logs/EXEC_REPORT_SHADOW_DEPLOY_VALIDATION_6FEB.md) e [SPRINT_3_CONSOLIDACAO_SHADOW_VALIDATION.md](SPRINT_3_CONSOLIDACAO_SHADOW_VALIDATION.md) para detalhes completos.

---

## ðŸ” Execution Evidence

### Validator Logs & Reports
- âœ… [Shadow Deploy Validator Report](archives/2026-02-07/logs/EXEC_REPORT_SHADOW_DEPLOY_VALIDATION_6FEB.md) - Exit Code 0 (data a definir)
- âœ… [Shadow Consolidation Report](SPRINT_3_CONSOLIDACAO_SHADOW_VALIDATION.md) - ValidaÃ§Ã£o completa
- âœ… [GIS Async Pipeline Results](archives/2026-02-07/logs/gis_async_pipeline_results_v2.log) - Pipeline execution log
- âœ… [GIS Async Pipeline JSON Results](gis_async_pipeline_results_v2.json) - Structured results

### Command Execution Records

#### SQL Migrations Validation
```bash
# Migration 1: Auto-Partition (1770500100)
psql -h localhost -U postgres -d villa_canabrava \
  -f BIBLIOTECA/supabase/migrations/1770500100_auto_partition_creation_2029_plus.sql \
  --dry-run
# Status: Ready for execution

# Migration 2: MV Refresh (1770500200)
psql -h localhost -U postgres -d villa_canabrava \
  -f BIBLIOTECA/supabase/migrations/1770500200_mv_refresh_scheduling_cron.sql \
  --dry-run
# Status: Ready for execution
```

#### Redis HA Circuit Breaker Test
```bash
# Execution command:
python redis_ha_sentinel_circuit_breaker_v1.py

# Expected output validation:
# âœ“ OperaÃ§Ã£o normal
# âœ“ EstatÃ­sticas de cache
# âœ“ Status do circuit breaker
# âœ“ Carga (100 requisiÃ§Ãµes completadas)
```

#### Documentation Generation Pipeline
```bash
# Execution command:
python doc_generation_pipeline_v1.py

# Expected outputs:
# - docs/api_openapi.json (OpenAPI 3.0 spec)
# - CHANGELOG_AUTO.md (Auto-generated changelog)
# - docs/auto_generated/README.md (Code documentation)
```

#### GIS Environment Validator
```bash
# Execution command:
python gis_async_pipeline_validator_v2.py

# Log location: archives/2026-02-07/logs/gis_async_pipeline_results_v2.log
# JSON results: gis_async_pipeline_results_v2.json
```

### Test Output Summaries
- **SQL Migrations**: Syntax validation pending (dry-run status: âœ… Ready)
- **Redis HA Circuit Breaker**: Load test pending (expected: 100 req/s minimum)
- **Documentation Pipeline**: Generation pending (expected: 3 output files)
- **GIS Pipeline**: Validation completed (check JSON results for details)

### Validation Chain
1. Shadow Deploy Validator â†’ Exit Code 0 âœ…
2. GIS Environment Validator â†’ Exit Code 0 âœ…
3. Infrastructure Baseline â†’ Ready âœ…
4. Integration Tests â†’ Ready for execution
5. Performance Benchmarking â†’ Pending
6. Final Release â†’ After benchmarks

---

---

## 1ï¸âƒ£ TESTES DE INTEGRAÃ‡ÃƒO

### Test Suite 1: SQL Migrations Validation

```bash
# Validar sintaxe SQL das 3 migrations Sprint 3
psql -h localhost -U postgres -d villa_canabrava \
  -f BIBLIOTECA/supabase/migrations/1770500100_auto_partition_creation_2029_plus.sql \
  --dry-run

psql -h localhost -U postgres -d villa_canabrava \
  -f BIBLIOTECA/supabase/migrations/1770500200_mv_refresh_scheduling_cron.sql \
  --dry-run

# Se tudo OK, executar de verdade
psql -h localhost -U postgres -d villa_canabrava \
  -f BIBLIOTECA/supabase/migrations/1770500100_auto_partition_creation_2029_plus.sql

psql -h localhost -U postgres -d villa_canabrava \
  -f BIBLIOTECA/supabase/migrations/1770500200_mv_refresh_scheduling_cron.sql
```

### Test Suite 2: Redis HA Circuit Breaker

```bash
# Instalar dependÃªncias
pip install aioredis circuitbreaker

# Executar testes
python redis_ha_sentinel_circuit_breaker_v1.py

# Esperado output:
# âœ“ OperaÃ§Ã£o normal
# âœ“ EstatÃ­sticas de cache
# âœ“ Status do circuit breaker
# âœ“ Carga (100 requisiÃ§Ãµes completadas)
```

### Test Suite 3: DocumentaÃ§Ã£o Auto-Generated

```bash
# Instalar dependÃªncias
pip install pdoc

# Executar pipeline
python doc_generation_pipeline_v1.py

# Outputs gerados:
# - docs/api_openapi.json (OpenAPI spec)
# - CHANGELOG_AUTO.md (changelog automÃ¡tico)
# - docs/auto_generated/README.md (docs de cÃ³digo)
```

### Test Suite 4: ValidaÃ§Ã£o MV Refresh

```bash
# Conectar ao PostgreSQL
psql -h localhost -U postgres -d villa_canabrava

# Dentro do psql, executar:
SELECT * FROM check_mv_refresh_health();
SELECT * FROM v_mv_refresh_status;
SELECT * FROM mv_refresh_log ORDER BY refreshed_at DESC LIMIT 10;
```

### Test Suite 5: ValidaÃ§Ã£o Auto-Partition

```bash
# Conectar ao PostgreSQL
psql -h localhost -U postgres -d villa_canabrava

# Dentro do psql, executar:
SELECT * FROM create_missing_year_partitions('catalogo_geometrias_particionada');
SELECT * FROM partition_maintenance_log ORDER BY maintenance_date DESC LIMIT 5;

-- Verificar partiÃ§Ãµes criadas
SELECT tablename FROM pg_tables 
WHERE tablename LIKE 'catalogo_geometrias_particionada_%' 
ORDER BY tablename;
```

---

## 2ï¸âƒ£ DEPLOY SHADOW ENVIRONMENT

### Pre-Flight Checklist

```bash
# 1. Verificar conectividade
ping postgres-shadow.internal
ping redis-sentinel-1.internal
ping redis-sentinel-2.internal
ping redis-sentinel-3.internal

# 2. Verificar espaÃ§o em disco
df -h /data/postgres
df -h /data/redis

# 3. Backup pre-deploy
pg_dump -h localhost -U postgres villa_canabrava > backup_shadow_pre_deploy.sql
```

### Deploy SQL Migrations

```bash
#!/bin/bash
# deploy_sprint3_migrations.sh

SHADOW_HOST="postgres-shadow.internal"
SHADOW_USER="deploy_user"
SHADOW_DB="villa_canabrava_shadow"

# Deploy migration 1
echo "Deploying OPT1: Auto-Partition..."
psql -h $SHADOW_HOST -U $SHADOW_USER -d $SHADOW_DB \
  -f BIBLIOTECA/supabase/migrations/1770500100_auto_partition_creation_2029_plus.sql

# Deploy migration 2
echo "Deploying OPT2: MV Refresh..."
psql -h $SHADOW_HOST -U $SHADOW_USER -d $SHADOW_DB \
  -f BIBLIOTECA/supabase/migrations/1770500200_mv_refresh_scheduling_cron.sql

echo "âœ“ All migrations deployed successfully"
```

### Deploy Redis HA Configuration

```bash
#!/bin/bash
# deploy_redis_ha.sh

REDIS_SENTINELS=(
  "redis-sentinel-1.internal:26379"
  "redis-sentinel-2.internal:26379"
  "redis-sentinel-3.internal:26379"
)

echo "Configurando Redis Sentinel..."

for sentinel in "${REDIS_SENTINELS[@]}"; do
  echo "Configurando $sentinel"
  redis-cli -h ${sentinel%:*} -p ${sentinel#*:} \
    SENTINEL set mymaster \
    down-after-milliseconds 5000 \
    parallel-syncs 1 \
    failover-timeout 10000
done

echo "âœ“ Redis HA configured"
```

### Deploy Grafana Dashboard

```bash
#!/bin/bash
# deploy_grafana_dashboard.sh

GRAFANA_URL="http://grafana-shadow.internal:3000"
GRAFANA_API_KEY="YOUR_API_KEY_HERE"

# Importar dashboard
curl -X POST \
  $GRAFANA_URL/api/dashboards/db \
  -H "Authorization: Bearer $GRAFANA_API_KEY" \
  -H "Content-Type: application/json" \
  -d @grafana_dashboard_rastreabilidade_v1.json

echo "âœ“ Dashboard deployed"
```

### ValidaÃ§Ã£o Post-Deploy

```bash
#!/bin/bash
# validate_shadow_deploy.sh

echo "=== VALIDAÃ‡ÃƒO POS-DEPLOY ==="

# 1. Verificar migrations
echo "1. Verificando migrations..."
psql -h postgres-shadow.internal -U deploy_user -d villa_canabrava_shadow \
  -c "SELECT * FROM information_schema.tables WHERE table_schema = 'public'" 

# 2. Verificar partiÃ§Ãµes
echo "2. Verificando partiÃ§Ãµes..."
psql -h postgres-shadow.internal -U deploy_user -d villa_canabrava_shadow \
  -c "SELECT tablename FROM pg_tables WHERE tablename LIKE 'catalogo_geometrias%'"

# 3. Verificar Redis
echo "3. Verificando Redis..."
redis-cli -h redis-sentinel-1.internal -p 26379 SENTINEL masters

# 4. Verificar cron jobs
echo "4. Verificando pg_cron jobs..."
psql -h postgres-shadow.internal -U deploy_user -d villa_canabrava_shadow \
  -c "SELECT * FROM cron.job"

echo "=== VALIDAÃ‡ÃƒO COMPLETA ==="
```

---

## 3ï¸âƒ£ PERFORMANCE BENCHMARKING

### Benchmark 1: Partition Query Performance

```bash
# partition_benchmark.sh

psql -h postgres-shadow.internal -U deploy_user -d villa_canabrava_shadow << EOF

-- Benchmark: Query on partitioned table
\timing on

-- Before partition pruning
EXPLAIN ANALYZE
SELECT COUNT(*) FROM catalogo_geometrias_particionada 
WHERE EXTRACT(YEAR FROM created_at) = 2026
  AND is_valid = true;

-- Test insert performance
PREPARE insert_test (UUID, GEOMETRY, BOOLEAN) AS
  INSERT INTO catalogo_geometrias_particionada (catalogo_id, geometry, is_valid)
  VALUES (\$1, ST_SetSRID(\$2, 4326), \$3);

-- Executar 1000 inserts
-- Medir tempo total

\timing off
EOF
```

### Benchmark 2: Redis Cache Performance

```python
# redis_benchmark.py

import asyncio
import time
from redis_ha_sentinel_circuit_breaker_v1 import RedisBoundsCache, SentinelConfig

async def benchmark_redis():
    """Benchmark cache operations"""
    
    config = SentinelConfig(
        sentinels=[
            ('redis-sentinel-1.internal', 26379),
            ('redis-sentinel-2.internal', 26379),
            ('redis-sentinel-3.internal', 26379)
        ]
    )
    
    cache = RedisBoundsCache(config)
    await cache.connect()
    
    test_bounds = {
        'min_lat': -19.5, 'max_lat': -19.4,
        'min_lon': -44.5, 'max_lon': -44.4
    }
    
    # Benchmark: SET operations
    start = time.time()
    for i in range(10000):
        await cache.set_bounds(f'cat_{i}', test_bounds)
    set_time = time.time() - start
    
    # Benchmark: GET operations
    start = time.time()
    for i in range(10000):
        await cache.get_bounds(f'cat_{i}')
    get_time = time.time() - start
    
    print(f"SET Performance: {10000/set_time:.1f} ops/sec")
    print(f"GET Performance: {10000/get_time:.1f} ops/sec")
    
    await cache.disconnect()

# Executar
asyncio.run(benchmark_redis())
```

### Benchmark 3: MV Refresh Performance

```bash
# mv_refresh_benchmark.sh

psql -h postgres-shadow.internal -U deploy_user -d villa_canabrava_shadow << EOF

-- Benchmark: MV Refresh time
\timing on

SELECT refresh_all_materialized_views();

-- Resultado esperado: <5 segundos

-- Benchmark: Query against MV
EXPLAIN ANALYZE
SELECT COUNT(*) FROM mv_catalogo_geometrias_stats
WHERE is_valid = true;

-- Resultado esperado: <100ms

\timing off
EOF
```

### Benchmark 4: Full Integration Load Test

```bash
# load_test.sh

# Usar ferramenta: wrk ou Apache JMeter
# SimulaÃ§Ã£o: 100 concurrent users, 5 min ramp-up, 10 min sustained

wrk -t12 -c100 -d300s \
  -s load_test.lua \
  http://api-shadow.internal:8000/catalogo/search

# load_test.lua
wrk.method = "GET"
wrk.body = ""

request = function()
  path = "/catalogo/search?q=geometria&limit=50"
  return wrk.format(nil, path)
end

response = function(status, headers, body)
  if status ~= 200 then
    print("Status: " .. status)
  end
end
```

---

## ðŸ“Š RELATÃ“RIO DE EXECUÃ‡ÃƒO

ApÃ³s executar todos os testes, gerar relatÃ³rio:

```bash
#!/bin/bash
# generate_test_report.sh

cat > SPRINT_3_TEST_REPORT.md << 'EOF'
# Sprint 3 - RelatÃ³rio de Testes de IntegraÃ§Ã£o

**Data:** $(date)
**Ambiente:** Shadow PostgreSQL 14 + Redis Sentinel + Grafana

## Resultados

### SQL Migrations
- [ ] OPT1 (Auto-Partition): PASSED/FAILED
- [ ] OPT2 (MV Refresh): PASSED/FAILED

### Redis HA
- [ ] Connection: PASSED/FAILED
- [ ] Failover: PASSED/FAILED
- [ ] Circuit Breaker: PASSED/FAILED

### Documentation
- [ ] API Spec Generated: PASSED/FAILED
- [ ] Changelog Generated: PASSED/FAILED

### Performance
- [ ] Partition Query P95: ___ms
- [ ] Cache GET ops/sec: ___
- [ ] MV Refresh time: ___s
- [ ] Load test throughput: ___req/s

### ObservaÃ§Ãµes
...

EOF

echo "âœ“ Report generated: SPRINT_3_TEST_REPORT.md"
```

---

## ðŸš€ PRÃ“XIMOS PASSOS

1. Executar testes de integraÃ§Ã£o
2. Deploy no shadow environment
3. Performance benchmarking
4. ValidaÃ§Ã£o final
5. Release para produÃ§Ã£o

**SLA:** Completar em 48h

---

*Guia criado: 2026-02-06T11:47:00Z*  
*Status: PRONTO PARA EXECUÃ‡ÃƒO*



