# ROLLOUT PLAN - 4 WEEKS (FEB 6)
## Sprint 3 Production Rollout

**Goal:** Deploy OPT1-5 safely with checkpoints and rollback readiness.

---

## Week 1 - OPT1 (Temporal Partitioning)
- Deploy OPT1 in staging
- Validate metrics (Q5 improvement >= 29%)
- Run rollback test (OPT1)
- Stakeholder update
- Go/No-Go for production OPT1

## Week 2 - OPT2 (Columnar Storage)
- Deploy OPT2 in staging
- Validate performance deltas
- Rollback test (OPT2)
- Go/No-Go for production OPT2

## Week 3 - OPT3 + OPT4
- Deploy OPT3 (RPC indexed views)
- Deploy OPT4 (auto partition 2029+)
- Validate metrics and query plans
- Rollback tests
- Go/No-Go for production OPT3/OPT4

## Week 4 - OPT5 (MV Refresh Scheduling)
- Deploy OPT5 in staging
- Validate cron jobs and MV refresh
- Rollback test (OPT5)
- Final production sign-off

---

## Checkpoints
- Pre-deploy: backup + monitoring ready
- Post-deploy: metrics + error rate check
- Rollback: <= 5 minutes per OPT
- Stakeholder comms after each week
