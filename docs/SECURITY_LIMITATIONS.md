# Security and reliability limitations

- This is a trusted local process and synthetic SQLite application, not an isolation sandbox for malicious Python or a production authorization service.
- Exact commands are supported; general natural-language task interpretation and semantic ambiguity handling are not implemented.
- File title mutation is the only write tool. Stored sensitivity is not a completed disclosure enforcement system; no email/share tool is executable yet.
- No human approval records, expiration, recipient grants or clarification controller exist. Reserved schema values are not evidence of those workflows.
- Duplicate action IDs are refused, but general idempotency keys and timeout-after-commit email recovery are pending.
- Unexpected errors remain OUTCOME_UNKNOWN without automatic retries. A process crash can leave EXECUTING records; startup reconciliation is pending.
- Invalid schema/unknown-tool requests fail before execution but currently lack a durable malformed-proposal audit record.
- The local API trusts the operator and all local processes. Origin/host checks do not establish authenticated users. Do not expose it publicly or run multiple workers.
- Incorrect trusted policy or scope can permit harmful actions. Retrieved content can still mislead model text even when protected mutations are denied.
- Ordinary records omit file bodies, but direct requests and titles are stored. Use synthetic data exclusively; no log mechanism here guarantees removal of all possible secrets entered by an operator.
- Benchmark, cross-model transfer, classifier calibration and research novelty claims remain unverified. A passing runtime suite is not universal AI safety evidence.

See [threat model](THREAT_MODEL.md), [policy](POLICY_ENGINE.md), and [recovery](EXECUTION_RECOVERY.md) for established and planned boundaries.
