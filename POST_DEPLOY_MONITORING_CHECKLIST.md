# POST-DEPLOY MONITORING CHECKLIST
## Mundo Virtual Villa Canabrava - OPT1-5

**Window:** First 24-72h after deploy
**Goal:** Validate performance, stability, and data integrity

---

## 0-1 Hour (Immediate)
- [ ] Confirm DB connectivity
- [ ] Verify key tables and partitions exist
- [ ] Check application error logs (0 critical errors)
- [ ] Validate Q5 query latency target
- [ ] Confirm rollback scripts accessible

---

## 1-4 Hours (Stability)
- [ ] Monitor QPS throughput trend
- [ ] Monitor cache hit ratio
- [ ] Check slow query log
- [ ] Validate GIS queries Q1-Q10 (no regressions)
- [ ] Confirm scheduled jobs (if OPT5 enabled)

---

## 4-24 Hours (Performance)
- [ ] Compare baseline vs current metrics
- [ ] Validate partition pruning in EXPLAIN ANALYZE
- [ ] Check index usage on key queries
- [ ] Confirm no increase in lock waits
- [ ] Validate replication/backup jobs

---

## 24-72 Hours (Confidence)
- [ ] Trend analysis for latency and QPS
- [ ] Validate error rate remains stable
- [ ] Stakeholder update sent
- [ ] Final sign-off recorded

---

## Metrics to Track
- Q5 latency (target: >= 29% improvement)
- Overall latency (target: >= 36.6% improvement)
- QPS throughput (target: >= 39.1% improvement)
- Cache hit ratio (target: +4.1%)
- Error rate (target: 0 critical)

---

## Rollback Criteria
- Sustained latency regression > 10%
- Error rate increase > 2x baseline
- Data integrity failure

---

## Notes
- If rollback required, use ROLLBACK_OPT1-5 scripts
- Log all actions and timestamps in rastreabilidade
