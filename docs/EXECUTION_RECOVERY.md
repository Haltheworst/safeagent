# Execution monitoring and recovery

## Implemented guarantees in the local simulator

Execution records persist action/task/tool, validated arguments, resolved IDs, policy decision and evaluated resource version, attempt count, timestamps, redacted result, error classification and verified flag. Valid denied calls persist BLOCKED with zero attempts. Unique action IDs reject repeats rather than performing them again; this is not a general idempotency-key receipt implementation.

The implemented successful path is PROPOSED → VALIDATING → APPROVED → EXECUTING → SUCCEEDED. APPROVED here denotes a policy-allowed action, not human approval. BLOCKED, FAILED and OUTCOME_UNKNOWN are distinct terminal outcomes for the current controller. Invalid transitions raise errors. The declared graph also reserves clarification, approval, cancellation and recovery paths for their future controllers.

An EXECUTING intent commits before tool entry. Each current tool runs in a SQLite transaction. Verification failure or an invalid response rolls back its local mutation. A matching resource-version predicate protects updates. The final local side effect and verified receipt commit atomically.

Known application validation/lookup/stale/permission errors record FAILED. Unexpected exceptions conservatively record OUTCOME_UNKNOWN. No automatic retry exists in v0.1. If a commit response fails but a durable SUCCEEDED receipt can be read, the gateway preserves it. If the database itself remains inaccessible, failure-record persistence can also fail; no successful completion should be inferred.

Task completion is verified separately. A completed read followed by a failed rename reports PARTIAL. Full tasks are serialized against reset in the single API process.

## Pending work

Fault schedules, explicit idempotency keys, email receipts, timeout-after-send reconciliation, bounded retries/backoff, all seven recovery strategies, dependencies, compensation and startup crash reconciliation are SA-026–SA-032. Tests simulating an unknown exception are not evidence of external timeout-after-commit recovery. An abrupt process crash can leave an EXECUTING record requiring future reconciliation.

For external tools, local rollback cannot undo a committed send. Implement authoritative operation receipts or supported idempotency before retrying. If evidence cannot determine the outcome, keep it unknown and escalate. Compensation must itself be authorized and must account for irreversible effects.
