# STAGE 4 - BASELINE VALIDATION REPORT (FEB 6)
## File: METRICS_BASELINE_FEB7.json

**Date:** 2026-02-06

---

## Baseline File Status
- **File present:** yes
- **Path:** METRICS_BASELINE_FEB7.json
- **Batch ID:** 550e8400-e29b-41d4-a716-446655440000
- **Database (metadata):** BIBLIOTECA
- **Host (metadata):** localhost:5432
- **GIS features (metadata):** 251

---

## Metrics Summary (from file)
- **Avg latency:** 73.62 ms
- **Throughput:** 214.5 QPS
- **Cache hit:** 89.1% (I/O)
- **Queries:** Q1-Q10 present (10/10)

---

## Validation Outcome
**Status:** PARTIAL

**Reason:** Local DB `biblioteca` has no `geometrias` table, so baseline metrics cannot be validated against current data.

---

## Next Actions
1. Load GIS dataset into local DB.
2. Re-run baseline collection (if needed).
3. Confirm query results and proceed to OPT1-5 measurements.
