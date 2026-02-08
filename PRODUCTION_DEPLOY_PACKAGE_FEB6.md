# PRODUCTION DEPLOY PACKAGE - FEB 6
## Mundo Virtual Villa Canabrava - OPT1-5 Rollout

**Status:** GO decision - approved for production
**Maintenance Window:** 20:00-02:00 local (est.)
**Estimated Duration:** 15-30 minutes

---

## Target (Confirmed)
- DB_HOST: host.docker.internal
- DB_PORT: 5432
- DB_NAME: BIBLIOTECA
- DB_USER: postgres
- DB_PASSWORD: [managed via secrets]

---

## Deployment Options

### Option A - Automatic (Executor) [SELECTED]
- Script: STAGE4_FULL_SIMULATOR.py
- Mode: OPT1-5 sequential with metrics and reports

### Option B - Manual (Runbook)
- Runbook: RUNBOOK_OPT1_PRODUCTION_ROLLOUT.md

---

## Pre-Deploy Checklist
- [x] Target host confirmed (DB_HOST)
- [ ] Secrets available (DB_PASSWORD)
- [ ] Maintenance window confirmed
- [ ] Backup plan ready (pg_dump)
- [ ] Rollback scripts verified (OPT1-5)
- [ ] Monitoring ready (latency/QPS/cache hit)
- [ ] Stakeholders notified

---

## Deploy Steps (High Level)
1. Pre-flight connection check
2. Backup database
3. Apply OPT1
4. Validate schema and data integrity
5. Collect OPT1 metrics
6. Application smoke tests
7. Continue OPT2-OPT5 if using automatic option
8. Post-deploy monitoring and validation

---

## Rollback Plan
- Scripts: ROLLBACK_OPT1-5_*.sql
- Target: BIBLIOTECA
- Expectation: full rollback < 5 minutes per OPT

---

## Post-Deploy Monitoring (24/7)
- Q5 latency
- Overall query latency
- QPS throughput
- Cache hit ratio
- Error rates / application logs

---

## Validation Criteria
- 0 regressions in Q1-Q10
- Q5 improvement >= 29%
- No application errors
- Data integrity consistent

---

## References
- STAGE4_FULL_SIMULATOR.py
- RUNBOOK_OPT1_PRODUCTION_ROLLOUT.md
- ROLLBACK_OPT1-5_*.sql
- archives/2026-02-07/logs/STAGE4_MASTER_STATUS.md



