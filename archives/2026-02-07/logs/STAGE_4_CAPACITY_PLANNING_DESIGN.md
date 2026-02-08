# 📊 STAGE 4: Capacity Planning - Design & Roadmap
## Mundo Virtual Villa Canabrava - Sprint 3

**Data de Planejamento:** 6 FEB 2026 18:30 UTC-3  
**Timeline de Execução:** 7-10 FEB 2026 (4 dias úteis)  
**Status:** 🔵 EM DESIGN (APROVAÇÃO PENDENTE)  

---

## 📋 EXECUTIVE SUMMARY

### Objetivos de STAGE 4

STAGE 4 valida a viabilidade de produção das 5 otimizações (OPT1-OPT5) através de **benchmarking rigoroso** em 6 eixos estratégicos:

1. **Performance das otimizações** - Quantificar ganhos latência/throughput/percentis
2. **Eficiência de particionamento** - Validar cobertura de partições e pruning hit rate
3. **Performance de refresh MVs** - Garantir <5 min de refresh sem impacto em produção
4. **Capacidade RPC Search** - Testar 1000 calls simultâneas com P95 <200ms
5. **Overhead de auto-partition** - Validar trigger <2% CPU durante peak hours
6. **Sizing de recursos** - Estabelecer CPU/Memory/Storage/Network para 3 cenários

**Resultado Final:** Documentação completa para sign-off de produção com Go/No-Go decision clara.

---

### Timeline de Execução

| Dia | Data | Foco Principal | Horas | Status |
|-----|------|-----------------|-------|--------|
| **Dia 1** | Feb 7 | Benchmarking Setup + Baseline | 8h | 🔵 PLANEJADO |
| **Dia 2** | Feb 8 | OPT1-5 Performance Tests | 8h | 🔵 PLANEJADO |
| **Dia 3** | Feb 9 | RPC Deep Dive + Auto-Partition Stress | 8h | 🔵 PLANEJADO |
| **Dia 4** | Feb 10 | Resource Estimation + Sign-off | 8h | 🔵 PLANEJADO |

---

### Equipe & Responsabilidades

| Agente | Responsabilidade | Eixo(s) |
|--------|------------------|---------|
| **Agent-DB** | OPT1-2 benchmarking + partitioning metrics | Eixo 1, 2, 5 |
| **Cache** | OPT5 MV refresh + scheduling validation | Eixo 3 |
| **Observability** | Grafana dashboards + Prometheus metrics | Todos |
| **Docs** | Consolidação de resultados + sign-off documentation | Todos |
| **Executor/Orquestrador** | Coordenação diária + escalação L1/L2/L3 | Governance |

---

### Critical Success Factors

| # | CSF | Métrica de Sucesso | Owner |
|---|-----|-------------------|-------|
| 1 | Baseline coletado | 100% das 6 métricas com dados T0 | Observability |
| 2 | OPT1-5 testadas em paralelo | Resultados comparativos 5 otimizações | Agent-DB |
| 3 | RPC validado sob carga | P95 <200ms com 1000 calls simultâneas | Cache |
| 4 | Auto-partition testado | Overhead <2% CPU durante trigger ativação | Agent-DB |
| 5 | Recursos estimados | 3 cenários documentados (S/M/L) | Docs |
| 6 | Sign-off completo | Checklist 6/6 passando + Go decision | Executor |

---

## 🗓️ ROADMAP: 4 Dias (FEB 7-10)

### ⚙️ Dia 1: FEB 7 - Benchmarking Setup + Baseline Collection

**Objetivo:** Estabelecer ambiente de teste e coletar métricas baseline (sem otimizações)

#### Manhã (09:00-12:00 UTC)

**09:00 - KICKOFF & Ambiente Setup**
- Daily Sync #1 (todos os agentes, 30 min)
- Verificar Grafana + Prometheus rodando
- Validar dataset: 251 GIS features carregadas
- Confirmar 100+ queries de teste disponíveis

**10:00 - Baseline Metrics Collection (Sem OPT1-5)**
- Agent-DB: Executar suite de testes contra banco ORIGINAL (sem otimizações)
- Coletar:
  - Query latency (p50, p95, p99) para cada query tipo
  - Throughput (QPS) máximo sustentável
  - CPU/Memory/IO utilization durante testes
  - Partition scan count (baseline, sem particionamento)
- Observability: Exportar métricas para Prometheus (tag: baseline-feb7)

**11:30 - Checkpoint Morning**
- Morning standup de 30 min
- Validar se baseline foi coletada 100%
- Documentar blockers (se houver)

#### Tarde (12:00-17:00 UTC)

**12:00 - RPC Search Baseline (Sem OPT3)**
- Cache: Executar 100 RPC search calls sequenciais (sem load)
- Medir: latência p50/p95/p99, throughput base
- Documentar função search_catalogo() performance

**14:00 - Auto-Partition Baseline (Sem OPT4)**
- Agent-DB: Verificar trigger overhead sem dados 2029+
- Medir CPU/Memory idle de auto-partition structures
- Estabelecer baseline <0.1% CPU overhead

**15:00 - MV Refresh Baseline (Sem OPT5)**
- Cache: Medir tempo de cálculo dinâmico sem MVs
- Baseline de CPU/IO durante query de bounds complexas
- Documentar expected cost de materialização

**16:00 - Consolidação & Armazenamento**
- Docs: Consolidar todos os números baseline em `METRICS_BASELINE_FEB7.json`
- Observability: Salvar dashboards Grafana com baseline snapshot
- Validar: 6 métricas baseline documentadas

**17:00 - Evening Status**
- Status report de 30 min (Executor/Orquestrador)
- Revisão: Todos os dados baseline foram coletados?
- Next day readiness

---

### 🚀 Dia 2: FEB 8 - OPT1-OPT5 Performance Tests

**Objetivo:** Executar benchmarks de cada otimização e medir performance gains

#### Manhã (09:00-12:00 UTC)

**09:00 - Daily Sync #2**
- Briefing rápido (baseline finalizado?)
- Plan para testes paralelos de OPT1-5
- Timeout policy: Qualquer teste >60s cancela e documenta

**10:00 - OPT1 & OPT2 Benchmarking (Agent-DB - Paralelo)**

**OPT1: Temporal Partitioning Benchmark**
- Ativar OPT1 em ambiente de teste (catalogo_geometrias_particionada)
- Executar 100+ queries com filtros temporais (2026-2028)
- Medir:
  - Query latency vs baseline: target >40% redução
  - Partition pruning hit rate: target >95%
  - Index scan count: target <5 partições por query
  - EXPLAIN ANALYZE para 10 queries representativas
- Grafana: Plot latency comparison (baseline vs OPT1)

**OPT2: Columnar Storage Benchmark**
- Ativar OPT2 (catalogo_bounds_cache + mv_catalogo_geometrias_stats)
- Executar 50 bounds queries e 50 geometry stats queries
- Medir:
  - Cache hit rate: target >95%
  - Latency improvement vs dynamic calc: target >60%
  - Storage compression: columnar format size vs original
  - Materialized view refresh time: time to refresh all MVs

**11:30 - Checkpoint & Intermediate Results**
- Agent-DB: Parar e consolidar OPT1/OPT2 resultados
- Observability: Conferir gráficos Grafana
- Continue ou escalate?

#### Tarde (12:00-17:00 UTC)

**13:00 - OPT3, OPT4, OPT5 Benchmarking**

**OPT3: Indexed Views + RPC Search Benchmark**
- Ativar mv_catalogo_search_indexed + search_catalogo_indexed() RPC
- Executar 100 RPC search calls com queries variadas
- Medir:
  - RPC latency p50/p95/p99: target p95 <100ms
  - Throughput (RPC/s): baseline measurement
  - Full-text search performance: indexed vs scan
  - Relevance ranking quality (qualitative)

**OPT4: Auto-Partition Creation Overhead**
- Validar trigger auto_create_partition_for_year()
- Medir overhead em operações INSERT:
  - Extra CPU cycles: target <2% overhead
  - Lock contention: target zero lock waits
  - Index creation time para novo ano: <5 segundos
- Teste: Simular INSERT para 2029 (trigger ativação)

**OPT5: MV Refresh Scheduling Performance**
- Validar pg_cron agendamentos
- Executar refresh_all_materialized_views() manualmente
- Medir:
  - Refresh time: target <5 minutos para MVs
  - Peak CPU durante refresh: target <20% CPU
  - Impact em queries concorrentes: target <5% latency increase
  - Cron job accuracy: verificar logs de execução

**16:00 - Consolidação de Resultados**
- Docs: Compilar comparativo 5 otimizações em tabela
- Formato: Baseline vs OPT1 vs OPT2 vs OPT3 vs OPT4 vs OPT5
- Cálcular % improvement para cada métrica

**17:00 - Evening Status**
- Status: OPT1-5 todos testados?
- Resultados confirmam 36.6% improvement de STAGE 2?
- Blockers para Dia 3?

---

### 🎯 Dia 3: FEB 9 - RPC Load Test + Auto-Partition Stress + Partitioning Deep Dive

**Objetivo:** Validar cenários extremos e eficiência de particionamento

#### Manhã (09:00-12:00 UTC)

**09:00 - Daily Sync #3**
- Quick check: OPT1-5 resultados OK?
- Plan para testes de carga + stress
- Team readiness para cenários extremos

**10:00 - RPC Search Load Test (1000 Concurrent Calls)**

Cache executa teste de capacidade RPC:
- Load test tool: Apache JMeter ou similiar
- Config: 1000 threads paralelos, 5 min duration
- Queries: Mix variado (search texto, filtro tipo, bounds queries)
- Medir:
  - P95 latency: target <200ms
  - P99 latency: target <500ms
  - Throughput: target >50 RPC/s
  - Error rate: target 0%
  - Database connection pool stress: target no overflow

**Cenário de Sobrecarga:** 2000 threads (double load)
- P95 latency degradation: target <3x vs 1000 threads
- Identify breaking point onde sistema falha

**11:30 - RPC Results Review**
- Cache: Análise de resultados
- Capacity calculation: Quantos usuários simultâneos suportados?
- Recomendações de connection pool sizing

#### Tarde (12:00-17:00 UTC)

**13:00 - Auto-Partition Stress Test (2029+ Growth Simulation)**

Agent-DB executa stress test de trigger auto-partition:
- Simulação: Inserir 10,000 registros com datas 2029-2035
- Monitor durante inserts:
  - CPU utilization por trigger execution
  - Lock contention (pg_stat_locks)
  - Index creation overhead (pg_stat_index_usage)
- Medir overhead em INSERT latency:
  - Target: <2% slowdown vs sem trigger

**OPT4 Trigger Validation:**
- Verificar novo ano partitions criadas automaticamente
- Validar índices criados em cada partição:
  - GIST em geometry ✓
  - Index em created_at DESC ✓
  - Composite em (catalogo_id, is_valid) ✓
- Test trigger failure scenario (se partição já existe)

**14:30 - Partitioning Efficiency Deep Dive**

Agent-DB analisa OPT1 + OPT4 eficiência:

**Métricas de Partitioning:**
- Partition coverage: % de queries que usam partition pruning
- Scan efficiency: Average partições scannadas por query (target <5)
- Index efficiency: GIST index hit rate (target >90%)
- Partition distribution: Data uniformemente distribuído nos anos?

**EXPLAIN ANALYZE de 20 Queries Críticas:**
- Para cada query: Extrair execution plan
- Validar que está usando partitions corretamente
- Documentar any queries que não aproveitam partitions
- Recomendações de indexing (se houver)

**Dashboard de Partition Health:**
- Grafana dashboard mostrando:
  - Partition sizes (2026, 2027, 2028)
  - Query scan count distribution
  - Index usage by partition
  - Partition pruning hit rate over time

**16:00 - Deep Dive Consolidation**
- Docs: Documentar partition health metrics
- Criar recommendations para optimization
- Validar: Todas partições <5 hits por query?

**17:00 - Evening Status**
- Status: RPC capacity + Auto-partition stress OK?
- Partition efficiency dentro de expectativa?
- Ready para Day 4 (resource estimation)?

---

### 📈 Dia 4: FEB 10 - Resource Estimation + Production Sizing + Sign-off

**Objetivo:** Finalizar análise e gerar sign-off de produção

#### Manhã (09:00-12:00 UTC)

**09:00 - Daily Sync #4 (FINAL)**
- All results from Days 1-3 coletados?
- Resource estimation team briefing
- Sign-off criteria review

**10:00 - Resource Estimation (CPU, Memory, Storage, Network)**

Docs + Agent-DB calculam recursos para 3 cenários:

**Cenário SMALL (100 usuários simultâneos, 251 GIS features)**
- CPU requirement:
  - Baseline (sem OPT): 2 vCPU
  - Com OPT1-5: 1 vCPU (50% redução esperada)
  - Margem de segurança: +1 vCPU overhead → 2 vCPU final
- Memory requirement:
  - Baseline buffers/cache: 4 GB
  - Com OPT2 (columnar) + indexes: +2 GB
  - Com OPT5 (MV materialization): +1 GB
  - Final: 7 GB RAM
- Storage:
  - Baseline: 10 GB
  - Compressão OPT2: -60% → 4 GB
  - Indexes overhead: +1 GB
  - Final: 5 GB storage
- Network:
  - Baseline throughput: 100 Mbps
  - Com RPC optimization (OPT3): reuse connections
  - Estimated BW: 50 Mbps (50% redução)

**Cenário MEDIUM (500 usuários simultâneos)**
- CPU: 4 vCPU
- Memory: 16 GB
- Storage: 12 GB
- Network: 200 Mbps

**Cenário LARGE (1000+ usuários simultâneos)**
- CPU: 8 vCPU
- Memory: 32 GB
- Storage: 25 GB
- Network: 400 Mbps

**Cost Estimation (Annual):**
- SMALL: ~$500/month = $6,000/year
- MEDIUM: ~$1,500/month = $18,000/year
- LARGE: ~$3,500/month = $42,000/year

#### Tarde (12:00-17:00 UTC)

**13:00 - Production Readiness Review**

Checklist de conformidade para sign-off:

| Eixo | Métrica | Status | Threshold | Result |
|------|---------|--------|-----------|--------|
| 1 | Query latency improvement | ⏳ | >30% vs baseline | ? |
| 1 | Throughput improvement | ⏳ | >25% vs baseline | ? |
| 1 | P95 latency reduction | ⏳ | >35% vs baseline | ? |
| 2 | Partition pruning hit rate | ⏳ | >95% | ? |
| 2 | Queries <5 partition scans | ⏳ | 100% compliance | ? |
| 2 | Index efficiency | ⏳ | >90% hit rate | ? |
| 3 | MV refresh time | ⏳ | <5 minutes | ? |
| 3 | Refresh CPU overhead | ⏳ | <5% peak impact | ? |
| 4 | RPC P95 latency | ⏳ | <200ms (1000 concurrent) | ? |
| 4 | RPC throughput | ⏳ | >50 RPC/s | ? |
| 5 | Auto-partition overhead | ⏳ | <2% CPU during trigger | ? |
| 6 | Resource sizing | ⏳ | 3 scenarios documented | ? |

**14:00 - Final Documentation & Audit Trail**

Docs team compila final documentation:
- METRICS_STAGE4_FINAL.json (todos os números)
- GRAFANA_DASHBOARDS_STAGE4.json (export de todos os dashboards)
- RESOURCE_MATRIX_SCENARIOS.md (sizing para S/M/L)
- PARTITION_HEALTH_REPORT.md (deep dive análise)
- RPC_LOAD_TEST_RESULTS.md (capacity findings)
- AUTO_PARTITION_STRESS_REPORT.md (2029+ simulation)

**15:00 - Go/No-Go Decision**

Executor/Orquestrador convoca sign-off committee:

**PASS Criteria (Go para Produção):**
- ✅ 6 eixos: 5+ de 6 com 100% success criteria
- ✅ Nenhum blocker crítico não-mitigado
- ✅ Documentação completa para auditoria
- ✅ Rollback plan validado (STAGE 3)

**FAIL Criteria (No-Go / Revisão):**
- ❌ Qualquer eixo com <80% success criteria
- ❌ RPC não passa load test (P95 >200ms ou error rate >0%)
- ❌ Auto-partition overhead >2%
- ❌ Resource estimation discrepâncias >20%

**15:30 - Sign-off Formal**

Documento assinado:
- **STAGE_4_CAPACITY_PLANNING_SIGNOFF.md**
  - Resultado de cada eixo
  - Go/No-Go decision + reasoning
  - Mitigações de qualquer blocker
  - Recomendações para STAGE 5 (Produção)

**16:00 - Handoff para STAGE 5**
- Docs: Entregar documentação para équipe de produção
- Agent-DB: Prepare rollback scripts (se No-Go)
- Executor: Schedule STAGE 5 kickoff (se Go)

**17:00 - FINAL Status**
- Fim de STAGE 4
- Resultado final documentado

---

## 🎯 EIXO 1: Benchmark Performance das 5 Otimizações (OPT1-OPT5)

### Descrição

Quantificar ganhos de performance de cada otimização individual (OPT1 a OPT5) através de benchmarking comparativo:
- Baseline (sem otimizações) vs cada OPT aplicada isoladamente
- Dataset: 251 GIS features com 100+ query patterns representativos
- Resultado: Tabela de improvements % com P50/P95/P99 latency breakdown

### Métricas Detalhadas

| Métrica | Descrição | Unidade | Target | Owner |
|---------|-----------|---------|--------|-------|
| **Query Latency (P50)** | Mediana de tempo de resposta | ms | >30% reduction | Agent-DB |
| **Query Latency (P95)** | 95º percentil (tail latency) | ms | >35% reduction | Agent-DB |
| **Query Latency (P99)** | 99º percentil | ms | >40% reduction | Agent-DB |
| **Throughput (QPS)** | Queries por segundo sustentável | QPS | +25% vs baseline | Agent-DB |
| **CPU Utilization** | CPU durante teste | % | <80% durante test | Observability |
| **Memory Usage** | RAM consumida | MB | baseline +10-20% acceptable | Observability |
| **Disk IO (IOPS)** | I/O operations | IOPS | 50% reduction vs baseline | Agent-DB |

### Ferramentas & Procedimentos

**Ferramentas:**
- **Grafana + Prometheus:** Dashboards de métricas em tempo real
- **PostgreSQL EXPLAIN ANALYZE:** Para validar execution plans
- **Apache JMeter/pgBench:** Load testing tools
- **Custom script (python):** Para orquestrar testes paralelos

**Procedimento Dia 2:**

```
T+0 min: Disable OPT1-5 (rollback para baseline)
T+5 min: Executar 100 queries (baseline) → Coletar P50/P95/P99
T+15 min: Enable OPT1 (temporal partitioning)
T+20 min: Executar mesmas 100 queries com OPT1 ativa
T+25 min: Comparar resultados, calcular % improvement
...
T+90 min: Todos OPT1-5 testados, resultados compilados
```

### Success Criteria

| Critério | Métrica | Limiar | Status |
|----------|---------|--------|--------|
| **Performance baseline** | Latency P95 coletada | >0 ms | ✓ |
| **OPT1 improvement** | Latency redução | >30% | ? |
| **OPT2 improvement** | Throughput aumento | >20% | ? |
| **OPT3 improvement** | Search latency | >50% | ? |
| **OPT4 não regride** | Insert latency overhead | <2% | ? |
| **OPT5 não regride** | Refresh impact | <5% CPU | ? |

### Blocker Risks & Mitigation

| Risk | Probabilidade | Impacto | Mitigation |
|------|--------------|--------|-----------|
| Queries não usam OPT indexes | MÉDIA | ALTO | Rewrite queries para forçar index usage |
| Dataset insuficiente (<251) | BAIXA | MÉDIO | Populat dados faltantes em Dia 1 |
| Métrica coleta falha | BAIXA | MÉDIO | Validar Prometheus setup no kickoff |
| OPT performance regride | BAIXA | CRÍTICO | Escalate para Agent-DB, revisar SQL |

### Dono da Execução

**Agent-DB** (com suporte Observability para Grafana)

### Documento Output Esperado

- `METRICS_OPT1_OPT5_COMPARISON_FEB8.md`
- Tabela comparativa: Baseline vs OPT1-5 (todas métricas)
- Gráficos latency por percentil (Grafana snapshot)
- Recomendações de combinações OPT que mais performam

---

## 🎯 EIXO 2: Análise de Partitioning Efficiency (OPT1 + OPT4)

### Descrição

Validar que particionamento temporal (OPT1) + auto-partition (OPT4) está funcionando otimalmente:
- Cobertura de partições: % de queries aproveitando partition pruning
- Partition scan efficiency: Média de partições scannadas por query (target <5)
- Índices GIST funcionando corretamente em cada partição

### Métricas Detalhadas

| Métrica | Descrição | Unidade | Target | Owner |
|---------|-----------|---------|--------|-------|
| **Partition Pruning Hit Rate** | % queries usando partition pruning | % | >95% | Agent-DB |
| **Avg Partitions per Query** | Média de partições scannadas | count | <5 | Agent-DB |
| **Index Hit Rate** | % de index scans vs seq scans | % | >90% | Agent-DB |
| **Partition Distribution** | Data uniformidade nos years | % | 30-40% cada | Agent-DB |
| **Scan Coverage** | % de data scannada efetivamente | % | <20% vs without partitions | Agent-DB |

### Ferramentas & Procedimentos

**Ferramentas:**
- **PostgreSQL EXPLAIN ANALYZE:** Para validar partition pruning nas execution plans
- **pg_stat_statements:** Para track partition usage stats
- **Grafana:** Dashboard de partition health
- **Custom query analyzer:** Script Python para parse 20 queries críticas

**Procedimento Dia 3:**

```
Parte 1: EXPLAIN ANALYZE de 20 queries críticas
  T+0: Para cada query, gerar EXPLAIN (JSON output)
  T+5: Parse execution plan, extract partition count
  T+10: Validate partition pruning is happening

Parte 2: Dashboard de partition health
  T+15: Criar Grafana dashboard com:
    - Partition size distribution (pie chart)
    - Query scan patterns (histogram)
    - Index usage by partition (bar chart)
    - Pruning hit rate trends (line chart)

Parte 3: Auto-partition (OPT4) validation
  T+45: Simulate 2029 data → trigger auto-create
  T+50: Verify new partition + indexes criados
  T+55: EXPLAIN queries com 2029 data → hit rate OK?
```

### Success Criteria

| Critério | Métrica | Limiar | Status |
|----------|---------|--------|--------|
| **Pruning habilitado** | Hit rate | >95% | ? |
| **Scans eficientes** | Avg partitions | <5 | ? |
| **Índices usados** | Hit rate GIST | >90% | ? |
| **Distribuição uniforme** | Year distribution | 30-40% | ? |
| **Auto-partition OK** | 2029 partição criada | ✓ | ? |

### Blocker Risks & Mitigation

| Risk | Probabilidade | Impacto | Mitigation |
|------|--------------|--------|-----------|
| Queries não usam partition pruning | MÉDIA | ALTO | Rewrite query WHERE clauses |
| Partition imbalance (1 year >80%) | BAIXA | MÉDIO | Reparticionar dados historicamente |
| Index GIST não criado auto | BAIXA | MÉDIO | Manual index creation em 2029 partition |
| Auto-partition trigger falha | BAIXA | CRÍTICO | Escalate, revisar trigger function |

### Dono da Execução

**Agent-DB** (com suporte Observability para Grafana)

### Documento Output Esperado

- `PARTITION_HEALTH_REPORT_FEB9.md`
- Tabela EXPLAIN ANALYZE para 20 queries (com partition count)
- Grafana dashboard snapshot (partition metrics)
- Recomendações de tuning (se hits <95%)

---

## 🎯 EIXO 3: MV Refresh Performance (OPT5)

### Descrição

Validar que scheduled materialized views (OPT5 + pg_cron) performam dentro de limites:
- Refresh time <5 minutos para o stack completo
- CPU overhead <5% durante refresh em contexto de queries concorrentes
- Cron scheduling accuracy (jobs executam no hora certa)

### Métricas Detalhadas

| Métrica | Descrição | Unidade | Target | Owner |
|---------|-----------|---------|--------|-------|
| **Full Refresh Time** | Tempo refresh all MVs | min | <5 min | Cache |
| **CPU Peak During Refresh** | CPU utilization pico | % | <20% peak | Observability |
| **Memory During Refresh** | RAM needed | MB | baseline +500 MB max | Observability |
| **Query Impact** | Latency increase queries concorrentes | % | <5% | Cache |
| **Cron Accuracy** | Job execution on-schedule | % | 100% | Observability |
| **Refresh Failure Rate** | % failed refreshes | % | 0% | Cache |

### Ferramentas & Procedimentos

**Ferramentas:**
- **pg_cron:** Built-in PostgreSQL task scheduler
- **PostgreSQL logs:** Para track refresh job execution
- **Grafana:** Monitor CPU/Memory durante refresh
- **Custom monitor script:** Track mv_refresh_log table

**Procedimento Dia 3:**

```
T+0 min: Setup monitoring (Grafana CPU/Memory gauges)
T+5 min: Disable auto cron jobs (manual test only)
T+10 min: Execute refresh_all_materialized_views() manualmente
T+15 min: Monitor:
  - Time to completion
  - Peak CPU (target <20%)
  - Peak Memory
  - Any query errors?
T+20 min: Check mv_refresh_log table (should show job completed)

T+25 min: Enable cron jobs
T+30 min: Monitor cron execution (3 jobs running):
  - refresh-mv-stats-hourly (0 * * * *)
  - refresh-mv-search-30min (*/30 * * * *)
  - refresh-mv-full-night (0 2 * * *)
  
T+60 min: Review logs de 3 execuções (should be 100% success)

T+90 min: Stress test - verificar impact em queries concorrentes
  - Start: Load test (100 QPS parallel queries)
  - Trigger: Manual refresh_all_materialized_views()
  - Measure: Latency increase during refresh
  - Target: <5% impact
```

### Success Criteria

| Critério | Métrica | Limiar | Status |
|----------|---------|--------|--------|
| **Refresh time OK** | Full refresh | <5 min | ? |
| **CPU aceitável** | Peak durante refresh | <20% | ? |
| **Memory OK** | Peak durante refresh | baseline +500 MB | ? |
| **Query impact minimal** | Latency increase | <5% | ? |
| **Cron acurado** | Execution on-schedule | 100% | ? |
| **Sem falhas** | Failure rate | 0% | ? |

### Blocker Risks & Mitigation

| Risk | Probabilidade | Impacto | Mitigation |
|------|--------------|--------|-----------|
| Refresh time >5 min | MÉDIA | ALTO | Otimizar MV definition (menos dados), split em 2 MVs |
| CPU overhead >5% | BAIXA | MÉDIO | Reschedule refresh para off-peak hours |
| Cron jobs não executando | BAIXA | CRÍTICO | Check pg_cron extension installed, check logs |
| Query latency degradation | BAIXA | MÉDIO | Increase READ replica capacity, or reschedule refresh |

### Dono da Execução

**Cache** (com suporte Agent-DB + Observability)

### Documento Output Esperado

- `MV_REFRESH_PERFORMANCE_REPORT_FEB9.md`
- Tabela: Refresh times + CPU/Memory metrics
- Cron job execution log (3 cron jobs, 100% success)
- Recomendações de schedule otimizado (se preciso ajustar)

---

## 🎯 EIXO 4: RPC Search Performance (OPT3)

### Descrição

Validar que indexed views + RPC search (OPT3) performam sob carga:
- 1000 RPC calls simultâneas: P95 <200ms, P99 <500ms
- Throughput >50 RPC/s sustentável
- 0% error rate
- Capacity estimation: Quantos usuários simultâneos suportados

### Métricas Detalhadas

| Métrica | Descrição | Unidade | Target | Owner |
|---------|-----------|---------|--------|--------|
| **RPC P95 Latency (1000 conc)** | 95º percentil resposta | ms | <200 ms | Cache |
| **RPC P99 Latency (1000 conc)** | 99º percentil resposta | ms | <500 ms | Cache |
| **Throughput (1000 conc)** | RPC calls/second | RPC/s | >50 RPC/s | Cache |
| **Error Rate (1000 conc)** | % failed calls | % | 0% | Cache |
| **Connection Pool Stress** | Max connections needed | count | <100 | Observability |
| **CPU During Load** | CPU utilization | % | <80% | Observability |
| **Breaking Point** | Max concurrent before 3x degradation | count | >1000 | Cache |

### Ferramentas & Procedimentos

**Ferramentas:**
- **Apache JMeter / Locust:** Load testing framework
- **Grafana:** Real-time latency/throughput monitoring
- **PostgreSQL connection stats:** pg_stat_activity
- **Custom load script:** Python/Node.js RPC client

**Procedimento Dia 3:**

```
T+0 min: Setup load test environment
  - JMeter configured with 1000 thread pool
  - Grafana dashboard live (latency, throughput, errors)
  - Database connection monitoring enabled

T+5 min: Warmup phase (100 concurrent, 2 min)
  - Establish connections
  - Cache initialization
  - Verify no errors

T+10 min: LOAD TEST PHASE 1 (1000 concurrent, 5 min)
  - Ramp up: 200 threads/min
  - Run 1000 threads in parallel
  - All threads issue mix of RPC queries:
    - search_catalogo_indexed(texto, tipo, geometric, limit, offset)
    - Variations: 50% bounds queries, 30% full-text, 20% filtered

T+15 min: Continuous monitoring
  - P95 latency (live graph)
  - Throughput (RPC/s)
  - Error rate
  - CPU on database
  - Connection count

T+20 min: Collect results
  - Raw latency histogram
  - Percentile breakdown (P50/P95/P99)
  - Throughput statistics
  - Error breakdown (if any)

T+25 min: STRESS TEST PHASE 2 (2000 concurrent, 3 min)
  - Double the load (2000 threads)
  - Measure: How much does performance degrade?
  - Target: P95 should go to <600ms (3x), not worse
  - Identify: Where does system break (error rate >5%)?

T+30 min: Cool down & recovery
  - Drop to 0 concurrent
  - Monitor: DB recovers to idle state?
  - No lingering connections?

T+35 min: Results consolidation
  - Parse JMeter results
  - Generate Grafana screenshot
  - Capacity calculation
```

### Success Criteria

| Critério | Métrica | Limiar | Status |
|----------|---------|--------|--------|
| **P95 latency OK** | 1000 concurrent | <200 ms | ? |
| **P99 latency OK** | 1000 concurrent | <500 ms | ? |
| **Throughput OK** | 1000 concurrent | >50 RPC/s | ? |
| **Error rate OK** | 1000 concurrent | 0% | ? |
| **Breaking point aceitável** | 2000 concurrent | P95 <3x vs 1000 | ? |
| **Connection pool OK** | Max connections | <100 | ? |

### Blocker Risks & Mitigation

| Risk | Probabilidade | Impacto | Mitigation |
|------|--------------|--------|-----------|
| P95 latency >200ms sob carga | MÉDIA | ALTO | Add read replicas, cache at application layer |
| Error rate >0% | BAIXA | CRÍTICO | Debug connection issues, reschedule load test |
| Connection pool overflow | BAIXA | MÉDIO | Increase PgBouncer pool size |
| CPU saturation | BAIXA | MÉDIO | Upgrade to larger database instance |

### Dono da Execução

**Cache** (com suporte Agent-DB + Observability)

### Documento Output Esperado

- `RPC_LOAD_TEST_RESULTS_FEB9.md`
- Tabela latency percentiles (P50/P95/P99) para 1000 e 2000 concurrent
- Grafana screenshot (latency, throughput, CPU live)
- Capacity calculation: N usuários simultâneos suportados
- Recomendações de connection pool + scaling

---

## 🎯 EIXO 5: Auto-Partition Overhead (OPT4)

### Descrição

Validar que auto-partition trigger (OPT4) não causa overhead significativo:
- Overhead na operação INSERT <2% vs sem trigger
- Trigger executa sem lock contention
- Auto-criação de índices funciona e não causa INSERT slowdown
- Teste simulando crescimento 2029+ (quando trigger será ativado)

### Métricas Detalhadas

| Métrica | Descrição | Unidade | Target | Owner |
|---------|-----------|---------|--------|--------|
| **INSERT Latency Overhead** | Slowdown due to trigger | % | <2% | Agent-DB |
| **Trigger Execution Time** | Time per trigger invocation | ms | <10 ms | Agent-DB |
| **Index Creation Time** | Auto-index para novo year | sec | <5 sec | Agent-DB |
| **Lock Contention** | Waits during trigger | count | 0 | Agent-DB |
| **CPU Peak** | CPU during trigger | % | <10% | Observability |
| **Memory Usage** | RAM during trigger | MB | baseline +50 MB | Observability |

### Ferramentas & Procedimentos

**Ferramentas:**
- **PostgreSQL pg_stat_locks:** Monitor lock contention
- **Custom insert script:** Parallel INSERT test
- **EXPLAIN ANALYZE:** Validate trigger execution path
- **Grafana:** CPU/Memory monitoring

**Procedimento Dia 3:**

```
PARTE 1: Baseline (Sem OPT4 - sem trigger)
T+0 min: Disable trigger auto_create_partition_for_year
T+5 min: Execute 10,000 INSERT statements (test year 2028)
  - Measure: Average INSERT latency
  - Target: <5ms per INSERT
  - Store as BASELINE_INSERT_LATENCY

PARTE 2: Com OPT4 (com trigger ativo)
T+10 min: Enable trigger
T+15 min: Execute 10,000 INSERT statements (test year 2028 - existing partition)
  - Measure: Average INSERT latency (trigger still checks if partition exists)
  - Target: <5.1ms (max 2% overhead)
  - Calculate: (latency_with_trigger / baseline) * 100

PARTE 3: Trigger Activation (Novo year 2029)
T+20 min: Execute INSERT com created_at = 2029-01-01
  - First INSERT triggers: create_missing_year_partitions()
  - Measure:
    - Trigger execution time
    - Index creation time (GIST + composite)
    - Lock contention (pg_locks)
    - CPU peak

T+25 min: Continue 2029 INSERTs (partition now exists)
  - Verify: Overhead volta a <2%

PARTE 4: Stress (Simulando 2029+ growth)
T+30 min: Parallel load test
  - 100 concurrent INSERTs to various 2029-2035 years
  - First INSERT per year triggers auto-create
  - Monitor:
    - Overall throughput (INSERTs/sec)
    - Lock contention
    - CPU/Memory peaks
    - Any failed INSERTs?
  - Target: No errors, overhead <2%
```

### Success Criteria

| Critério | Métrica | Limiar | Status |
|----------|---------|--------|--------|
| **INSERT overhead minimal** | vs baseline | <2% | ? |
| **Trigger fast** | Per invocation | <10 ms | ? |
| **Index creation fast** | Per new year | <5 sec | ? |
| **Sem lock contention** | pg_locks waits | 0 | ? |
| **CPU aceitável** | Peak durante trigger | <10% | ? |
| **Stress test OK** | 100 concurrent 2029+ | 0 errors | ? |

### Blocker Risks & Mitigation

| Risk | Probabilidade | Impacto | Mitigation |
|------|--------------|--------|-----------|
| Trigger overhead >2% | BAIXA | MÉDIO | Optimize function logic, consider partial indexes |
| Index creation locks writes | BAIXA | CRÍTICO | Use CONCURRENTLY index creation, retry logic |
| Lock contention detected | MUITO BAIXA | CRÍTICO | Escalate, redesign trigger |
| Trigger fails for 2029+ | MUITO BAIXA | CRÍTICO | Manual partition + index creation, disable trigger |

### Dono da Execução

**Agent-DB** (com suporte Observability)

### Documento Output Esperado

- `AUTO_PARTITION_STRESS_REPORT_FEB9.md`
- Tabela: Baseline vs com trigger (latency comparison)
- Trigger execution metrics (invocations, timing)
- Index creation log (2029-2035 partitions created)
- CPU/Memory graphs (Grafana snapshot)
- Recomendações (se overhead >2%, otimizations)

---

## 🎯 EIXO 6: Estimativa de Recursos para Produção

### Descrição

Consolidar todos os learnings dos Eixos 1-5 para estimar CPU/Memory/Storage/Network necessários em produção, para 3 cenários de escala (Small/Medium/Large).

### Métricas Detalhadas

| Métrica | Descrição | Unidade | SMALL | MEDIUM | LARGE |
|---------|-----------|---------|-------|--------|-------|
| **CPU Cores** | vCPU needed | cores | 2 | 4 | 8 |
| **Memory** | RAM allocation | GB | 7 | 16 | 32 |
| **Storage** | Disk space | GB | 5 | 12 | 25 |
| **Network BW** | Peak bandwidth | Mbps | 50 | 200 | 400 |
| **Concurrent Users** | Simultaneous capacity | users | 100 | 500 | 1000+ |
| **Monthly Cost** | Cloud cost estimate | $/mo | ~$500 | ~$1,500 | ~$3,500 |

### Cálculo por Cenário

#### **Cenário SMALL: 100 Usuários Simultâneos, 251 GIS Features**

**CPU Calculation:**
- Baseline (sem OPT): 2 vCPU needed para 100 concurrent
- Com OPT1-5: 50% reduction esperado → 1 vCPU
- Margem de segurança: +1 vCPU
- **Final: 2 vCPU**

**Memory Calculation:**
- PostgreSQL shared_buffers: 2 GB
- Working memory (work_mem × max_parallel): 1 GB
- OPT2 columnar cache (mv + bounds): 2 GB
- OPT5 materialized views: 1 GB
- OS + overhead: 1 GB
- **Final: 7 GB RAM**

**Storage Calculation:**
- Base GIS data: 10 GB
- OPT2 columnar compression: -60% → 4 GB
- Indexes (GIST, composite, full-text): +1 GB
- WAL logs + checkpoints: 500 MB
- **Final: 5 GB**

**Network Calculation:**
- RPC query BW: 100 Mbps baseline
- With OPT3 (connection reuse): 50% reduction
- **Final: 50 Mbps peak**

**Cost (AWS/GCP/Azure 2026 pricing):**
- 2 vCPU = ~$50/month
- 7 GB RAM = ~$150/month
- 5 GB storage = ~$1/month
- Network = ~$300/month (est.)
- **Total: ~$500/month = $6,000/year**

#### **Cenário MEDIUM: 500 Usuários Simultâneos**

Baseline → x5 escalation vs SMALL

- **CPU: 4 vCPU** (SMALL 2 × 2.5, minus 10% efficiency gain via OPT)
- **Memory: 16 GB** (SMALL 7 × 2, plus 2 GB cache growth)
- **Storage: 12 GB** (SMALL 5 × 2.4, data growth)
- **Network: 200 Mbps** (peak, sustained ~100 Mbps)
- **Cost: ~$1,500/month = $18,000/year**

#### **Cenário LARGE: 1000+ Usuários Simultâneos**

Baseline → x10 escalation vs SMALL

- **CPU: 8 vCPU** (SMALL 2 × 4.5, with efficiency from OPT)
- **Memory: 32 GB** (SMALL 7 × 4.5, cache + buffers)
- **Storage: 25 GB** (SMALL 5 × 5, compounded growth)
- **Network: 400 Mbps** (peak, sustained ~200 Mbps)
- **Cost: ~$3,500/month = $42,000/year**

### Ferramentas & Procedimentos

**Procedimento Dia 4:**

```
T+0 min: Consolidate all Eixo 1-5 metrics
  - Query latency improvement: % reduction
  - Partition scan efficiency: avg partitions per query
  - MV refresh overhead: % CPU impact
  - RPC capacity: N concurrent at P95 <200ms
  - Auto-partition overhead: % INSERT slowdown

T+10 min: Build resource matrix
  - For each scenario (S/M/L):
    - Calculate CPU from throughput (QPS at target P95)
    - Calculate Memory from indexes + cache size
    - Calculate Storage from data compression
    - Calculate Network from RPC BW + replication

T+30 min: Cost estimation
  - Research cloud pricing (AWS/GCP/Azure)
  - Calculate monthly cost per scenario
  - Annualize (×12 months)

T+45 min: Sensitivity analysis
  - What if OPT doesn't deliver 50% improvement?
  - What if user growth is 2x faster?
  - What if storage compression is only 40% not 60%?
  - Risk matrix: best/expected/worst case costs

T+60 min: Recommendations
  - For each scenario: Recommended instance types (AWS/GCP)
  - Recommended read replicas
  - Recommended backup strategy
  - Migration path (S → M → L)
```

### Success Criteria

| Critério | Métrica | Limiar | Status |
|----------|---------|--------|--------|
| **S sizing OK** | 100 users capacity | ✓ | ? |
| **M sizing OK** | 500 users capacity | ✓ | ? |
| **L sizing OK** | 1000+ users capacity | ✓ | ? |
| **Cost realistic** | Cloud pricing accuracy | ±20% | ? |
| **Sensitivity analysis** | Risk scenarios documented | all 3 covered | ? |

### Blocker Risks & Mitigation

| Risk | Probabilidade | Impacto | Mitigation |
|------|--------------|--------|-----------|
| OPT doesn't achieve 50% improvement | MÉDIA | ALTO | Recalculate with observed actual improvement |
| Cloud pricing changed | BAIXA | MÉDIO | Use multiple cloud vendors, estimate range |
| User growth faster than expected | BAIXA | MÉDIO | Design for L scenario upfront, plan upgrade path |
| Storage compression less than 60% | MÉDIA | MÉDIO | Recalculate with 40% compression, budget more storage |

### Dono da Execução

**Docs** (com suporte Agent-DB + Observability)

### Documento Output Esperado

- `RESOURCE_MATRIX_SCENARIOS_FEB10.md`
- Tabela detailed: CPU/Memory/Storage/Network/Cost para S/M/L
- Justificação de cada número (baseado em Eixo 1-5 results)
- Sensitivity analysis (best/expected/worst case)
- Recommended cloud instance types (AWS t3/m5, GCP n1/n2, Azure B/D)
- Migration path (how to scale from S → M → L)

---

## 🔗 INTEGRATION POINTS

### Daily Synchronization

#### **Daily Sync #1 - FEB 7, 09:00 UTC (Kickoff)**
- **Duração:** 30 min
- **Attendees:** Agent-DB, Cache, Observability, Docs, Executor/Orquestrador
- **Agenda:**
  - Ambiente setup validation (Grafana, Prometheus, dataset)
  - Role assignment confirmation
  - Baseline collection status
  - Blockers? Escalation needed?

#### **Daily Sync #2 - FEB 8, 09:00 UTC (Day 2)**
- **Duração:** 30 min
- **Agenda:**
  - Baseline collection: Complete? 6 métricas OK?
  - OPT1-5 test execution status
  - Preliminary results (if ready)
  - Adjustments needed for Day 3?

#### **Daily Sync #3 - FEB 9, 09:00 UTC (Day 3)**
- **Duração:** 30 min
- **Agenda:**
  - OPT1-5 results review
  - RPC load test + Auto-partition stress prep
  - Resource estimation timeline
  - Any metric validation issues?

#### **Daily Sync #4 - FEB 10, 09:00 UTC (Sign-off Day)**
- **Duração:** 30 min
- **Agenda:**
  - All results consolidated?
  - Resource matrix final numbers
  - Sign-off gate review (6 eixos OK?)
  - Go/No-Go decision date/time

### Daily Checkpoints

#### **Morning Standups - 09:00 UTC Cada Dia**
- 30 min: Daily sync (acima)
- Each agent: 3 min status (completed, blockers, next 24h plan)

#### **Evening Status Reports - 17:00 UTC Cada Dia**
- 30 min: Executor/Orquestrador convoca
- Metrics collected: Yes/No/Partial
- Blocker escalation: Any L1/L2/L3 needed?
- Readiness para próximo dia

### Escalation Policy

#### **Level 1 (Agente-to-Executor):**
- Trigger: Test failure, metric invalid, environment issue
- Response time: <1 hour
- Resolution: Executor coordinates fix, retry test

#### **Level 2 (Executor-to-Orquestrador):**
- Trigger: Test cannot recover, resource unavailable, timeline risk
- Response time: <2 hours
- Resolution: Orquestrador allocates resources, rescopes if needed

#### **Level 3 (Orquestrador-to-Decision Gate):**
- Trigger: Go/No-Go gate at risk, critical metric missing, architecture issue
- Response time: <4 hours
- Resolution: Executive sign-off, decision on continuation or pivot

---

## ✅ SIGN-OFF GATE (FEB 10, 15:00 UTC)

### Checklist de Conformidade (6 Eixos)

Todos os itens devem ser ✅ PASS para Go decisión:

#### **Eixo 1: Benchmark Performance OPT1-OPT5**

| Item | Métrica | Threshold | Status |
|------|---------|-----------|--------|
| Baseline coletado | 6 métricas P50/P95/P99 | ✓ | ⏳ |
| OPT1 improvement | Query latency P95 | >30% reduction | ⏳ |
| OPT2 improvement | Throughput | >20% increase | ⏳ |
| OPT3 improvement | Search latency | >50% reduction | ⏳ |
| OPT4 não regride | INSERT overhead | <2% | ⏳ |
| OPT5 não regride | Refresh CPU impact | <5% | ⏳ |
| **Eixo 1 Status** | **Pass/Fail** | **5/6 = Pass** | ⏳ |

#### **Eixo 2: Partitioning Efficiency**

| Item | Métrica | Threshold | Status |
|------|---------|-----------|--------|
| Pruning habilitado | Hit rate | >95% | ⏳ |
| Scans eficientes | Avg partitions per query | <5 | ⏳ |
| Índices usados | GIST hit rate | >90% | ⏳ |
| Distribuição uniforme | Year distribution | 30-40% each | ⏳ |
| Auto-partition OK | 2029 partition created | ✓ | ⏳ |
| **Eixo 2 Status** | **Pass/Fail** | **5/5 = Pass** | ⏳ |

#### **Eixo 3: MV Refresh Performance**

| Item | Métrica | Threshold | Status |
|------|---------|-----------|--------|
| Refresh time OK | Full refresh | <5 min | ⏳ |
| CPU aceitável | Peak during refresh | <20% | ⏳ |
| Memory OK | Peak during refresh | baseline +500 MB | ⏳ |
| Query impact minimal | Latency increase | <5% | ⏳ |
| Cron acurado | Execution on-schedule | 100% | ⏳ |
| Sem falhas | Failure rate | 0% | ⏳ |
| **Eixo 3 Status** | **Pass/Fail** | **6/6 = Pass** | ⏳ |

#### **Eixo 4: RPC Search Performance**

| Item | Métrica | Threshold | Status |
|------|---------|-----------|--------|
| P95 latency OK | 1000 concurrent | <200 ms | ⏳ |
| P99 latency OK | 1000 concurrent | <500 ms | ⏳ |
| Throughput OK | 1000 concurrent | >50 RPC/s | ⏳ |
| Error rate OK | 1000 concurrent | 0% | ⏳ |
| Breaking point acceptable | 2000 concurrent | P95 <3x degradation | ⏳ |
| Connection pool OK | Max connections | <100 | ⏳ |
| **Eixo 4 Status** | **Pass/Fail** | **6/6 = Pass** | ⏳ |

#### **Eixo 5: Auto-Partition Overhead**

| Item | Métrica | Threshold | Status |
|------|---------|-----------|--------|
| INSERT overhead minimal | vs baseline | <2% | ⏳ |
| Trigger fast | Per invocation | <10 ms | ⏳ |
| Index creation fast | Per new year | <5 sec | ⏳ |
| Sem lock contention | pg_locks waits | 0 | ⏳ |
| CPU aceitável | Peak durante trigger | <10% | ⏳ |
| Stress test OK | 100 concurrent 2029+ | 0 errors | ⏳ |
| **Eixo 5 Status** | **Pass/Fail** | **6/6 = Pass** | ⏳ |

#### **Eixo 6: Resource Estimation**

| Item | Métrica | Threshold | Status |
|------|---------|-----------|--------|
| SMALL scenario | 100 users, $6k/year | Documented | ⏳ |
| MEDIUM scenario | 500 users, $18k/year | Documented | ⏳ |
| LARGE scenario | 1000+ users, $42k/year | Documented | ⏳ |
| Sensitivity analysis | Best/Expected/Worst | Covered | ⏳ |
| Cloud pricing validated | AWS/GCP/Azure | ±20% accuracy | ⏳ |
| Migration path | S→M→L scaling | Documented | ⏳ |
| **Eixo 6 Status** | **Pass/Fail** | **6/6 = Pass** | ⏳ |

---

### Go/No-Go Decision Criteria

#### **GO to Production** ✅
Requer: **5/6 eixos com 100% pass** + nenhum blocker crítico não-mitigado

Significado:
- Otimizações performam conforme expectativa
- Não há surpresas de escalabilidade
- Documentação completa para rollback (STAGE 3 validado)
- Equipe confiante em produção

**Ação:** Proceder para STAGE 5 (Produção) com confiança

#### **NO-GO / Revisão** ❌
Requer: **<5/6 eixos passando** OU **blocker crítico não-mitigado**

Exemplos:
- RPC P95 latency >250ms (não passa test)
- Auto-partition overhead >3% (unacceptable)
- Resource estimation discrepâncias >30%
- Nenhuma mitigação viável

**Ação:** Escalate para Orquestrador, revisar architecture, reschedule STAGE 4

---

### Sign-off Document

Documento final: **`STAGE_4_CAPACITY_PLANNING_SIGNOFF.md`**

Contém:
1. **Executive summary:** Go/No-Go decision + reasoning
2. **Results table:** 6 eixos, métricas finais, pass/fail
3. **Mitigations:** Qualquer blocker identificado + solução
4. **Recommendations:** Para STAGE 5 produção
5. **Sign-offs:** Agent-DB, Cache, Observability, Docs, Executor/Orquestrador

---

## 📊 Diagrama de Fluxo - STAGE 4

```
┌─────────────────────────────────────────────────────────────┐
│          STAGE 4: CAPACITY PLANNING (Feb 7-10)              │
└─────────────────────────────────────────────────────────────┘

FEB 7 (Dia 1): SETUP + BASELINE
├── 09:00 Kickoff sync
├── 10:00 Baseline collection (sem OPT1-5)
│   ├── Query latency (P50/P95/P99)
│   ├── Throughput (QPS)
│   ├── CPU/Memory/IO utilization
│   └── RPC baseline (100 calls)
├── 14:00 MV + Auto-partition baseline
├── 16:00 Consolidation: METRICS_BASELINE_FEB7.json
└── 17:00 Evening status + Day 1 validation

FEB 8 (Dia 2): OPT BENCHMARKING
├── 09:00 Sync #2
├── 10:00 OPT1 + OPT2 tests (Agent-DB paralelo)
│   ├── Temporal partitioning gains
│   └── Columnar storage compression
├── 13:00 OPT3 + OPT4 + OPT5 tests
│   ├── RPC search performance
│   ├── Auto-partition overhead
│   └── MV refresh timing
├── 16:00 Consolidation: METRICS_OPT1_OPT5_FEB8.md
└── 17:00 Evening status + OPT results validation

FEB 9 (Dia 3): LOAD TESTS + DEEP DIVES
├── 09:00 Sync #3
├── 10:00 RPC Load Test (1000 concurrent)
│   ├── P95/P99 latency validation
│   ├── Throughput measurement
│   ├── Stress test (2000 concurrent)
│   └── Capacity calculation
├── 13:00 Auto-partition Stress (2029+)
│   ├── INSERT overhead validation
│   ├── Trigger execution metrics
│   └── Index creation timing
├── 14:30 Partitioning Deep Dive
│   ├── EXPLAIN ANALYZE (20 queries)
│   ├── Partition pruning validation
│   └── Grafana dashboard creation
├── 16:00 Consolidation: 3 reports (RPC, Auto-partition, Partition)
└── 17:00 Evening status + Readiness for sign-off

FEB 10 (Dia 4): RESOURCE ESTIMATION + SIGN-OFF
├── 09:00 Sync #4 (final)
├── 10:00 Resource Estimation (S/M/L scenarios)
│   ├── CPU/Memory/Storage/Network per scenario
│   ├── Cost estimation (AWS/GCP/Azure)
│   ├── Sensitivity analysis (best/expected/worst)
│   └── Migration path (S→M→L)
├── 13:00 Production Readiness Review
│   ├── Checklist validation (6 eixos)
│   ├── Blocker assessment
│   └── Mitigation confirmation
├── 15:00 Go/No-Go Decision
│   ├── Committee review (5 agents + Executor)
│   ├── Final approval
│   └── Sign-off document creation
├── 16:00 Handoff to STAGE 5 (if Go)
└── 17:00 STAGE 4 COMPLETE

Final Output Documents:
├── METRICS_BASELINE_FEB7.json
├── METRICS_OPT1_OPT5_COMPARISON_FEB8.md
├── RPC_LOAD_TEST_RESULTS_FEB9.md
├── AUTO_PARTITION_STRESS_REPORT_FEB9.md
├── PARTITION_HEALTH_REPORT_FEB9.md
├── MV_REFRESH_PERFORMANCE_REPORT_FEB9.md
├── RESOURCE_MATRIX_SCENARIOS_FEB10.md
└── STAGE_4_CAPACITY_PLANNING_SIGNOFF.md (Go/No-Go)
```

---

## 📝 Resumo de Entregáveis

| Documento | Owner | Due | Status |
|-----------|-------|-----|--------|
| METRICS_BASELINE_FEB7.json | Observability | Feb 7 EOD | 🔵 |
| METRICS_OPT1_OPT5_COMPARISON_FEB8.md | Agent-DB | Feb 8 EOD | 🔵 |
| RPC_LOAD_TEST_RESULTS_FEB9.md | Cache | Feb 9 EOD | 🔵 |
| AUTO_PARTITION_STRESS_REPORT_FEB9.md | Agent-DB | Feb 9 EOD | 🔵 |
| PARTITION_HEALTH_REPORT_FEB9.md | Agent-DB | Feb 9 EOD | 🔵 |
| MV_REFRESH_PERFORMANCE_REPORT_FEB9.md | Cache | Feb 9 EOD | 🔵 |
| RESOURCE_MATRIX_SCENARIOS_FEB10.md | Docs | Feb 10 EOD | 🔵 |
| STAGE_4_CAPACITY_PLANNING_SIGNOFF.md | Executor | Feb 10 15:00 | 🔵 |

---

## 📌 Notas Importantes

1. **Timeline Crítica:** 4 dias úteis = 32 horas operacionais. Qualquer delay em Day 1-3 afeta Day 4 sign-off.

2. **Documentação para Auditoria:** Todos os resultados devem ser rastreáveis:
   - Query execution times com timestamps
   - Grafana dashboard snapshots
   - Database logs relevantes
   - Load test raw data (JMeter results)

3. **Fallback Plan:** Se qualquer eixo falhar:
   - Escalar para Orquestrador imediatamente
   - Considerar re-test ou ajustar scope
   - Não forçar sign-off com dados incompletos

4. **Continuidade de STAGE 3:** Rollback scripts (STAGE 3) devem estar prontos:
   - Se No-Go: execute rollbacks para reversão
   - Se Go: arquivar scripts para emergency-only

---

**Documento de Design Preparado para Revisão e Aprovação.**

Status: 🔵 **EM DESIGN (Aguardando Aprovação do Usuário)**
