# Research log

## 2026-09-22 — foundation

Hypothesis: independent task/resource enforcement can prevent forbidden side effects even when the planner proposes them. The current deterministic security tests demonstrate only the implemented boundary under trusted-process assumptions. They do not establish comparative model-level efficacy.

Decision: begin with an exact read/rename command grammar and synthetic file tools. This makes task scope explicit while the general intent-confirmation layer is pending. Do not treat broad keyword matching as permission.

Decision: commit durable execution intent before tool entry; use an atomic local transaction for sandbox mutation and its verified receipt. External service receipts/idempotency require a separate implementation. Do not generalize SQLite rollback to irreversible email sends.

Decision: prepare a provisional 48-issue backlog because the individual referenced ticket definitions were absent. Do not fabricate GitHub mappings; authentication check failed.

Engineering references consulted: [FastAPI lifespan](https://fastapi.tiangolo.com/advanced/events/), [SQLAlchemy version counters](https://docs.sqlalchemy.org/en/20/orm/versioning.html), and [Vite setup](https://vite.dev/guide/). This code uses an explicit version predicate for updates and startup initialization through FastAPI lifespan. These references are implementation documentation, not a completed related-work survey.

Next research work: review primary agent/tool authorization, prompt-injection and transaction-recovery literature; identify comparable baselines; define state-based oracles and leakage-resistant scenario grouping before making novelty or performance claims. Independently reviewed human ML labels require an actual reviewer and must be reported as pending until obtained.
