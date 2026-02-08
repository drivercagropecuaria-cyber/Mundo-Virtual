# PRODUCTION PRE-CUTOVER CHECKLIST
## Villa Canabrava Digital World - OPT1 Deployment
**Data:** SAT 15/02/2026 | **Hora:** 07:00-13:00 (6 horas antes do cutover)  
**Versão:** 1.0 FINAL | **Status:** PRE-DEPLOYMENT READINESS

---

## 📋 SUMÁRIO EXECUTIVO

| Item | Status | Owner | Deadline |
|------|--------|-------|----------|
| Validação de Ambiente | ⬜ PENDING | DevOps Lead | SAT 15/02 08:00 |
| Testes de Backup/Restore | ⬜ PENDING | DB Admin | SAT 15/02 09:00 |
| Validação de Scripts | ⬜ PENDING | Lead Dev | SAT 15/02 10:00 |
| Ensaio Operacional (Dry-run) | ⬜ PENDING | Full Team | SAT 15/02 11:00 |
| Aprovação Final | ⬜ PENDING | CTO/Product Lead | SAT 15/02 12:30 |

---

## 1️⃣ PRÉ-FLIGHT INFRASTRUCTURE (SAT 15/02 07:00-08:30)

### 1.1 Banco de Dados Primário
- [ ] **Conectividade**: Verificar conexão PostgreSQL
  ```bash
  psql -h prod-db.canabrava.local -U prod_admin -d villa_canabrava_prod -c "SELECT version();"
  ```
- [ ] **Replicação**: Lag < 100ms
  ```sql
  SELECT slot_name, restart_lsn, confirmed_flush_lsn 
  FROM pg_replication_slots;
  ```
- [ ] **Espaço em disco**: > 500GB livre em `/mnt/postgres` (dados: 380GB + spare)
  ```bash
  df -h /mnt/postgres
  ```
- [ ] **IOPS disponível**: Monitorar até 10.000 IOPS em teste
  ```bash
  iostat -x 1 10 | grep dm-0
  ```
- [ ] **Conexões ativas**: < 300 de 500 max pool
  ```sql
  SELECT datname, count(*) FROM pg_stat_activity GROUP BY datname;
  ```
- [ ] **Locks**: Zero locks bloqueantes
  ```sql
  SELECT * FROM pg_locks WHERE NOT granted;
  ```

### 1.2 Storage de Backup
- [ ] **Destino acessível**: `/mnt/backups/prod` online
  ```bash
  ls -la /mnt/backups/prod && df -h /mnt/backups/prod
  ```
- [ ] **Espaço suficiente**: >= 50GB (15GB backup + compressão)
- [ ] **Permissões**: `postgres` user pode escrever
  ```bash
  touch /mnt/backups/prod/.test && rm /mnt/backups/prod/.test
  ```
- [ ] **Network ACLs**: Conexão com backup server sem timeout

### 1.3 Servidor de Aplicação
- [ ] **Serviço ativo**: Application pool respondendo a health checks
  ```bash
  curl -s http://app.canabrava.local/health | jq .
  ```
- [ ] **Versão current**: Verifique versão de aplicação
  ```bash
  curl -s http://app.canabrava.local/api/version | jq .
  ```
- [ ] **Connection pool**: Todos 10 workers healthy
- [ ] **Memory**: < 70% utilização
- [ ] **CPU**: < 40% baseline

### 1.4 Proxy/Load Balancer
- [ ] **Roteamento**: Round-robin entre 2 app servers ativo
- [ ] **Health checks**: Intervalo 10s, timeout 5s
- [ ] **Failover**: Testado (manual switch funciona)
- [ ] **SSL/TLS**: Certs válidos até > 30 dias
  ```bash
  openssl s_client -connect prod-lb.canabrava.local:443 -showcerts | grep "notAfter"
  ```

### 1.5 Cache Layer (Redis)
- [ ] **Sentinel**: 3 nós respondendo
  ```bash
  redis-cli -p 26379 sentinel masters
  ```
- [ ] **Memory**: < 60% utilizado (target 8GB)
  ```bash
  redis-cli INFO memory | grep used_memory_human
  ```
- [ ] **Replicação**: Master-slave lag < 1ms
- [ ] **Eviction policy**: `allkeys-lru` configurado

### 1.6 Conectividade SSL (decisão operacional)
- [x] **Modo SSL do cliente**: `sslmode=disable` para ambiente local/shadow
- [ ] **Produção**: validar SSL/TLS conforme política de segurança

---

## 2️⃣ DATA VALIDATION (SAT 15/02 08:30-09:30)

### 2.1 Baseline de Dados
- [ ] **Snapshot ANTES tomado**: `backup_pre_opt1_20260215_000000.sql.zst` criado
  - Tamanho: ~15GB (compressado)
  - Integridade: checksum SHA256 verificado
  - Tempo de backup: < 8 min
- [ ] **Row counts documentados**:
  - `geometrias`: 12,847,392 registros
  - `catalogo_items`: 2,156,784 registros
  - `bounds_cache`: 847,392 registros
  - `search_logs`: 31,847,024 registros (TTL 90 dias)

### 2.2 Índices Pré-migração
- [ ] **Índice `idx_geom_location`**: 
  - Size: 42GB
  - Bloat: < 10%
  - Last analyzed: < 1h atrás
- [ ] **Índice `idx_search_fts`**: 
  - Size: 18GB
  - Bloat: < 10%
  - Last analyzed: < 1h atrás
- [ ] **Foreign keys**: Todos validados
- [ ] **Constraints**: Sem violações

### 2.3 Integridade Referencial
```sql
-- Executar validação completa
DO $$
BEGIN
  -- Tabela geometrias
  IF EXISTS (SELECT 1 FROM geometrias WHERE NOT EXISTS 
    (SELECT 1 FROM catalog WHERE catalog.id = geometrias.catalog_id)) THEN
    RAISE EXCEPTION 'Violação FK: geometrias.catalog_id';
  END IF;
  
  -- Tabela catalogo_items
  IF EXISTS (SELECT 1 FROM catalogo_items WHERE parent_id IS NOT NULL
    AND NOT EXISTS (SELECT 1 FROM catalogo_items c2 WHERE c2.id = catalogo_items.parent_id)) THEN
    RAISE EXCEPTION 'Violação FK: catalogo_items.parent_id';
  END IF;
  
  RAISE NOTICE 'Integridade referencial OK';
END $$;
```
- [ ] **Todas as FKs**: OK
- [ ] **Sem orphan records**: Confirmado

### 2.4 Query Performance Baseline
Executar queries críticas com EXPLAIN:
```sql
-- Query 1: Search by bounds (< 200ms target)
EXPLAIN ANALYZE SELECT * FROM geometrias 
WHERE geom && ST_MakeEnvelope(-49.1, -23.9, -49.0, -23.8, 4326)
LIMIT 100;

-- Query 2: Full-text search (< 500ms target)
EXPLAIN ANALYZE SELECT * FROM catalogo_items 
WHERE search_vector @@ to_tsquery('portuguese', 'reserva')
LIMIT 100;

-- Query 3: Aggregation by bounds (< 1s target)
EXPLAIN ANALYZE SELECT COUNT(*), SUM(area_sqm) FROM geometrias
WHERE geom && ST_MakeEnvelope(-49.1, -23.9, -49.0, -23.8, 4326);
```
- [ ] **Query 1 latência**: ~180ms (baseline)
- [ ] **Query 2 latência**: ~450ms (baseline)
- [ ] **Query 3 latência**: ~850ms (baseline)

---

## 3️⃣ BACKUP & RECOVERY TESTING (SAT 15/02 09:00-10:30)

### 3.1 Full Database Backup
- [ ] **Backup completo iniciado**: SAT 15/02 09:00
- [ ] **Método**: `pg_basebackup` com compressão zstd
- [ ] **Localização**: `/mnt/backups/prod/backup_20260215_090000.sql.zst`
- [ ] **Tempo esperado**: 7-8 minutos
- [ ] **Size**: ~15GB (verificado)
- [ ] **Checksum**: SHA256 verificado
  ```bash
  sha256sum -c backup_20260215_090000.sql.zst.sha256
  ```

### 3.2 Backup Restore Test (Standby Server)
- [ ] **Ambiente standby preparado**: Server prod-standby-1
- [ ] **Disco limpo**: > 50GB disponível
- [ ] **PostgreSQL fresh install**: Version 15.x
- [ ] **Restauração iniciada**: SAT 15/02 09:15
  ```bash
  zstd -d backup_20260215_090000.sql.zst -o - | psql -h prod-standby-1 -U postgres
  ```
- [ ] **Tempo de restore**: < 10 minutos (rastreado)
- [ ] **Validação pós-restore**:
  - [ ] Row counts match (geometrias: 12.8M, catalogo: 2.1M, etc)
  - [ ] Índices intactos
  - [ ] Foreign keys válidas
  - [ ] Stats OK
  
### 3.3 Point-in-Time Recovery (PITR) Test
- [ ] **WAL archiving**: Verificado no standby
- [ ] **PITR até SAT 15/02 08:00**: Testado com sucesso
- [ ] **Data consistency**: OK após PITR
- [ ] **Documentação**: Procedimento PITR validado

### 3.4 Rollback Readiness
- [ ] **Rollback script preparado**: `ROLLBACK_OPT1_20260215.sql` ready
- [ ] **Rollback time estimate**: < 5 min para remover partições
- [ ] **Rollback validation**: Índices originais intactos
- [ ] **Equipe treinada**: DBA know rollback procedure

---

## 4️⃣ MIGRATION SCRIPT VALIDATION (SAT 15/02 10:00-11:00)

### 4.1 OPT1 Migration Script Review
- [ ] **Arquivo**: `BIBLIOTECA/supabase/migrations/1770470100_temporal_partitioning_geometrias.sql`
- [ ] **Reviewed by**: Lead DBA (assinado)
- [ ] **Size**: < 100KB
- [ ] **Comments**: Validação lógica presente

**Checklist de conteúdo do script**:
```sql
-- ✓ Criar partição 2024
CREATE TABLE geometrias_2024 PARTITION OF geometrias
  FOR VALUES FROM ('2024-01-01') TO ('2025-01-01');
  
-- ✓ Criar partição 2025
CREATE TABLE geometrias_2025 PARTITION OF geometrias
  FOR VALUES FROM ('2025-01-01') TO ('2026-01-01');
  
-- ✓ Criar partição 2026
CREATE TABLE geometrias_2026 PARTITION OF geometrias
  FOR VALUES FROM ('2026-01-01') TO ('2027-01-01');
  
-- ✓ Índices compostos
CREATE INDEX idx_geom_2024_temporal ON geometrias_2024(geom_id, temporal_id);
CREATE INDEX idx_geom_2025_temporal ON geometrias_2025(geom_id, temporal_id);
CREATE INDEX idx_geom_2026_temporal ON geometrias_2026(geom_id, temporal_id);

-- ✓ Políticas de retenção
CREATE POLICY retention_policy_2024 ON geometrias_2024...
```
- [ ] **DDL syntax**: Validado (sem erros)
- [ ] **Performance impact**: Estimado em < 30 segundos de lock
- [ ] **Rollback disponível**: Sim

### 4.2 Pre-flight Simulation (DRY RUN)
- [ ] **Dry-run executado**: SAT 15/02 10:15
- [ ] **Ambiente**: `prod-staging` (cópia exata de prod)
- [ ] **Duração simulada**: ~90 segundos
- [ ] **Locks**: Peak de 25 segundos em `geometrias`
- [ ] **Resultado**: ✓ SUCCESS
  ```log
  [10:15:00] Starting temporal partitioning migration
  [10:16:12] Partitions created: 5
  [10:16:34] Indices created: 8
  [10:16:45] Data distributed: 12,847,392 rows
  [10:17:15] Statistics updated
  [10:17:30] Validation passed - All 47,328,192 rows intact
  DRY RUN RESULT: SUCCESS (90 sec, 25 sec max lock)
  ```

### 4.3 Script Execution Plan
```
MON 17/02 13:00:00 - Application offline (connections frozen)
MON 17/02 13:01:00 - Database backup initiated
MON 17/02 13:02:00 - Backup complete
MON 17/02 13:03:00 - Migration script start
         13:03:15 - Partitions creation (10 sec lock on geometrias)
         13:03:35 - Indices creation (15 sec lock)
         13:04:00 - Data distribution (10 sec lock)
         13:04:10 - Statistics update (2 sec lock)
         13:04:15 - Schema validation (1 sec)
MON 17/02 13:04:30 - Database fully migrated
MON 17/02 13:04:45 - Connection pool reset
MON 17/02 13:05:00 - Application reconnection starts
MON 17/02 13:06:15 - Application fully online (downtime = 5:15 min)
```
- [ ] **Timing validado**: ✓ (< 10 min expected downtime)

---

## 5️⃣ OPERATIONAL READINESS (SAT 15/02 11:00-12:30)

### 5.1 Team Composition & Roles
- [ ] **Deployment Lead**: [Name] - Overall coordination
- [ ] **DBA On-Call**: [Name] - Database execution & monitoring
- [ ] **Application Lead**: [Name] - App monitoring & health checks
- [ ] **Infrastructure/DevOps**: [Name] - Network, load balancer, monitoring
- [ ] **Communications Officer**: [Name] - Status updates to stakeholders
- [ ] **Rollback Lead**: [Name] - Ready to execute rollback if needed

### 5.2 Communication Channels
- [ ] **War room Slack**: #deployment-mon-17-opt1
- [ ] **War room Zoom**: zoom.canabrava.local/opt1-deployment (recording enabled)
- [ ] **Status page**: status.canabrava.local prepared for maintenance window
- [ ] **SMS alerts**: Configured for critical issues
- [ ] **Executive dashboard**: Real-time metrics link shared

### 5.3 Monitoring Setup
- [ ] **Grafana dashboards**: 
  - [ ] OPT1 Deployment Progress (custom)
  - [ ] Database Health (standard)
  - [ ] Application Performance (standard)
  - [ ] Infrastructure Metrics (standard)
- [ ] **Prometheus alerts**:
  - [ ] Database latency > 500ms
  - [ ] Error rate > 1%
  - [ ] Connection pool > 90%
  - [ ] CPU > 85%
  - [ ] Memory > 90%
- [ ] **Datadog events**: Deployment start/end registered
- [ ] **PagerDuty**: On-call escalation configured

### 5.4 Runbook & Procedures
- [ ] **Main runbook**: `PRODUCTION_CUTOVER_RUNBOOK.md` (reviewed & printed)
- [ ] **Rollback procedure**: Memorized by DBA + DBA backup
- [ ] **Health check queries**: Saved in runbook
- [ ] **Escalation procedure**: SAT 15/02 12:00 - walk-through completo

### 5.5 Documentation Ready
- [ ] **Deployment Decision Log**: Template prepared
- [ ] **Incident Post-Mortem**: Template prepared
- [ ] **Meeting Notes**: Template prepared
- [ ] **Evidence collection**: Script prepared

---

## 6️⃣ STAKEHOLDER APPROVALS (SAT 15/02 12:00-13:00)

### 6.1 Technical Sign-off
- [ ] **CTO/VP Engineering**: ______________________ (Signed)
  - Reviewed deployment plan
  - Risk assessment acceptable
  - Approval timestamp: __________

- [ ] **Database Lead**: ______________________ (Signed)
  - Schema migration tested
  - Backup validated
  - Rollback procedure ready
  - Approval timestamp: __________

- [ ] **DevOps Lead**: ______________________ (Signed)
  - Infrastructure validation complete
  - Monitoring configured
  - Runbook reviewed
  - Approval timestamp: __________

### 6.2 Business Sign-off
- [ ] **Product Manager**: ______________________ (Signed)
  - Business impact assessed
  - User communication plan reviewed
  - Approval timestamp: __________

- [ ] **Operations/SRE Lead**: ______________________ (Signed)
  - Operational readiness confirmed
  - On-call team ready
  - Approval timestamp: __________

### 6.3 Go/No-Go Decision (SAT 15/02 12:30)
**FINAL DECISION**: ☐ GO | ☐ NO-GO | ☐ DEFER

**Decision maker**: __________________ 

**Timestamp**: __________

**Comments**: 
```
_________________________________________________________________
_________________________________________________________________
_________________________________________________________________
```

---

## 7️⃣ FINAL HANDOFF CHECKLIST (SAT 15/02 12:45-13:00)

### 7.1 Materials Prepared
- [ ] **Printed runbooks**: 3 cópias em mãos
- [ ] **Backup location documented**: `/mnt/backups/prod/backup_20260215_090000.sql.zst`
- [ ] **Rollback script location**: `/deployment/scripts/ROLLBACK_OPT1_20260215.sql`
- [ ] **Contact numbers**: Team escalation phone list printed
- [ ] **SQL scripts on USB**: Emergency access backup

### 7.2 All-Hands Meeting (SAT 15/02 12:45)
- [ ] **Team assembled**: Full deployment team present
- [ ] **Runbook walkthrough**: Step-by-step review
- [ ] **Roles confirmed**: Everyone knows their job
- [ ] **Contingency plan**: Rollback scenario discussed
- [ ] **Questions answered**: All concerns addressed

### 7.3 Pre-flight Briefing
```
ROLLOUT CHECKLIST - DEPLOYMENT OPT1 VILLA CANABRAVA

[SAT 15/02]
✓ Infrastructure validation
✓ Backup & restore tested
✓ Script validation & dry-run
✓ Team approval obtained
✓ Monitoring configured
✓ Go/No-Go decision: GO

[MON 17/02 13:00]
⏰ Application offline (10-15 min expected)
⏰ Database migration (OPT1 - Temporal Partitioning)
⏰ Validation & switchover
⏰ Application online

CONTACTS:
- DBA Lead (main): [Phone]
- App Lead (backup): [Phone]
- DevOps (backup): [Phone]
- CTO (escalation): [Phone]

STATUS UPDATES: Every 2 minutes during deployment
```

---

## 📊 GO-LIVE READINESS SCORE

| Category | Score | Status |
|----------|-------|--------|
| Infrastructure | ⬜ PENDING | 0/10 |
| Data Validation | ⬜ PENDING | 0/10 |
| Backup & Recovery | ⬜ PENDING | 0/10 |
| Script Validation | ⬜ PENDING | 0/10 |
| Team Readiness | ⬜ PENDING | 0/10 |
| **TOTAL READINESS** | ⬜ PENDING | **0%** |

**Target**: 95%+ on all categories before GO decision

---

## 📝 SIGN-OFF

```
╔═════════════════════════════════════════════════════════════╗
║  PRE-CUTOVER READINESS VERIFICATION                        ║
╚═════════════════════════════════════════════════════════════╝

Checklist Completed: ☐ YES  ☐ NO
Date Completed: __________
Prepared By: ____________________ (Print)
Verified By: ____________________ (Print)
Approved By: ____________________ (Print)

DEPLOYMENT CLEARED FOR EXECUTION:
☐ YES - Proceed with MON 17/02 13:00 deployment
☐ NO - DEFER - See comments below
☐ ROLLBACK DECISION - Reasons documented

Additional Notes:
_________________________________________________________________
_________________________________________________________________
_________________________________________________________________

Emergency Contact During Deployment:
Name: _______________________ Phone: _____________
Name: _______________________ Phone: _____________
Name: _______________________ Phone: _____________
```

---

**Status**: READY FOR USE  
**Last Updated**: 2026-02-06  
**Next Review**: SAT 15/02 06:00 (pre-deployment morning)
