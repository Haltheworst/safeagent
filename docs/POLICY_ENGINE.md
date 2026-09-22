# Policy engine

The trusted controller stores a task with user/session ownership, granted operations, permitted resource IDs and an exact mutation object. The gateway loads this context from storage. The model cannot pass an authorization context through the tool schema or modify it through an API endpoint.

## Initial command scope

`Read FILE-001` grants READ_FILE on that resource within the task. `Rename FILE-001 to New title` grants READ_FILE and WRITE_FILE on that resource and binds the change to `{"file_id":"FILE-001","changes":{"title":"New title"}}`. A complete anchored grammar is used, never unrestricted keyword matching. All other input is rejected with an honest explanation of mock-mode limitations. General natural-language interpretation will propose scopes requiring trusted confirmation.

Server ACLs remain necessary even for an explicit user command. USER-001 has read/write entries for FILE-001 and FILE-003; FILE-002 belongs to USER-002 and has no grants to USER-001. The `owner_id` is descriptive; the ACL is the authority for access in this release.

## Decision order

1. Validate registered tool and strict arguments; reject session/target claims that disagree.
2. Load an active task owned by the trusted user/session.
3. Check tool enabled by configuration, task operation, task resource, resource existence and server ACL.
4. For a mutation, compare its concrete effect with stored scope and validate policy title length/version.
5. Persist decision and block without tool entry, or persist executing intent and reevaluate under the database lock.

This release emits ALLOW/BLOCK. Invalid arguments are `ProposalValidationError`, not BLOCK. Invalid trusted identity raises `PermissionError`. These pre-execution interface errors currently have no durable per-action audit record; expanding validation auditing is part of SA-012/SA-017.

## Configuration and reasons

`config/default.json` allows the two registered tools. `config/strict.json` permits reads only. Configuration is parsed with a strict typed schema. Core reason codes: `TOOL_DISABLED`, `TASK_OPERATION_DENIED`, `TASK_RESOURCE_DENIED`, `RESOURCE_NOT_FOUND`, `RESOURCE_PERMISSION_DENIED`, `TASK_EFFECT_DENIED`, `TITLE_POLICY_DENIED`, `STALE_RESOURCE_STATE`, `AUTHORIZED`.

To add an operation, register explicit schemas, execution and verification functions; define its trusted scope and resource/recipient rules; then add a policy and observed-state tests. Merely listing a tool in policy configuration does not implement it or grant a task authority.

## Pending approval and disclosure work

No approval endpoint or grants exist yet. A forged `approved` argument is rejected. Schema presence of REQUIRE_APPROVAL does not mean approvals work. SA-022 will bind a single-use grant to canonical tool arguments, exact resource version, recipients, attachments, side effects and expiry. Non-overridable denials must precede approval. Sensitivity metadata is currently stored; full recipient/disclosure rules are pending because no disclosure tool is registered.
