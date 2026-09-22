# Architecture — foundation release

## Implemented vertical slice

`TaskService` is a trusted application controller. It accepts a deliberately constrained user command, persists a task and exact authorization scope, and invokes `MockAgent`. The mock planner knows the task input, registry contract and observations; it never receives a SQLAlchemy session. The only agent-facing execution method is `Gateway.execute(proposal, trusted_identity)`.

The gateway validates tool arguments with Pydantic, loads task ownership from SQLite, resolves the concrete resource, and evaluates declarative policy, operation permission, task resource scope, server-side ACL, exact mutation payload and resource version. The proposal's explanation and claimed evidence never grant permission. Unsupported names cannot be dispatched.

On ALLOW, execution intent is committed before tool entry. In a new SQLite `BEGIN IMMEDIATE` transaction, the gateway reloads trusted context and reevaluates the policy. A registered tool runs, its typed response is validated, and its verification function checks actual state. The local database mutation, redacted receipt and SUCCEEDED state commit in one transaction. This atomicity covers only this simulator's local database operation; it does not imply atomic email/calendar workflows or external-service transactions.

`TaskService` then evaluates completion using durable execution records and actual file state. A successful read followed by a failed rename produces PARTIAL. A blocked adversarial proposal does not prevent reporting the legitimate read as complete, and the report separately states the refusal.

## Boundaries and data flow

| Component | Trust | Authority |
| --- | --- | --- |
| Local operator and task controller | Trusted | Creates exact command scope |
| Model/mock proposals and retrieved content | Untrusted | Can propose registered operations only |
| Policy configuration, ACL database and identity | Trusted | Determines permission |
| Tool functions and state verifier | Trusted | Mutates/reads synthetic database |
| Operator inspection API | Trusted local surface | Inspects synthetic metadata; unavailable to the model |

Ordinary audit records omit document content and the arbitrary agent explanation. Read output retains source ID and `UNTRUSTED_SANDBOX_CONTENT`. Metadata/title and the direct user request are persisted; use only synthetic input.

## Concurrency and lifecycle

The application uses one process, a reentrant process lock, and SQLite write transactions. Full tasks are serialized against resets. Resource updates include a version predicate. Running multiple API workers, multiple independent server instances, or untrusted code in the process is unsupported. Production requires authenticated sessions, distributed coordination, durable job ownership, crash reconciliation, protected storage and service-specific receipt semantics.

The state machine defines all specified states; only validation, allow/block, execution, success, failure and unknown-outcome paths are exercised in v0.1. Waiting/approval/recovery states are vocabulary for future controllers, not implemented workflows. On unexpected errors the gateway records an unknown outcome and does not retry. A process crash can leave EXECUTING records; startup reconciliation is pending.

## Module map

- `agent/agent.py`: constrained trusted command parser, mock planner and verified task controller.
- `runtime/`: strict proposals, trusted contexts, policy rules, state transitions and gateway.
- `sandbox/`: SQLAlchemy models, explicit registry and synthetic fixtures.
- `bootstrap.py`, `migrations/`: source-checkout initialization and versioned schema.
- `main.py`, `cli.py`: loopback operator API and CLI.
- `frontend/`: real task submission, trace inspection, reset and resource metadata.

No model provider, baseline bypass, email/calendar domain, external sharing, risk ML, research runner or general-purpose tools are implemented. Expand these in dependency order rather than bypassing the established boundary.
