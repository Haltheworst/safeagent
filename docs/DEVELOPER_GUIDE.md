# Developer guide

Use [the backlog](GITHUB_ISSUES.md) as the dependency plan. The next dependency-ready domain issue is SA-003: expand versioned fixtures for email, contacts, calendar, folders and files. SA-001/SA-002 foundation work must remain passing while expanding the domain.

## Add a tool

Define strict argument and response models, an explicit application function and an observed-state verifier. Register all safety metadata. Extend trusted scope creation and server ACL/policy rules for its concrete effects. Add security tests that spy on dispatch and compare snapshots. Do not expose the raw tool function, database handle, unrestricted network or shell to the agent.

Add schema changes in a new Alembic revision; never rewrite an applied migration in a published release. Keep fixtures stable and versioned. Use the gateway's transaction model only for actual local database operations; external tools need separate idempotency/receipt semantics.

Run `python scripts/dev.py check` using the development virtual environment. For formatting, `python scripts/dev.py format`. The optional local pre-commit configuration uses the active Python environment; hook installation is not required for ordinary setup.

## API/Python usage

`bootstrap(Settings(...))` applies migrations and seeds a local database. `TaskService(gateway).run("Read FILE-001")` provides the current end-to-end interface. Integrators using `Gateway.execute` must supply trusted identities and persist tasks from application code; never deserialize those grants from a model response.

External provider integration is planned in SA-010. Keep provider transport errors, budgets and usage separate from tool errors. Use offline transport fixtures for CI and opt-in live-model tests. No credentials should be in proposals or ordinary logs.
