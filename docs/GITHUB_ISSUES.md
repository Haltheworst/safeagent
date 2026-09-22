# GitHub issue mirror

Remote repository, milestones, labels, board and issues have **not been created**. On 2026-09-22, `gh auth status` reported an invalid stored token. No remote URL or issue number is invented.

The supplied specification referenced 48 issues without including their individual definitions. This is a **provisional specification-derived backlog**, not a claim to preserve unseen issue wording. [backlog.json](backlog.json) is the structured import source; each linked local ticket has scope, acceptance criteria, tests, dependencies, documentation and definition of done. Remote references are null until confirmed.

## Local board

Backlog → Ready → In Progress → In Review → Done. `in-progress` includes partial vertical-slice work; it does not establish milestone completion. Verified local work will be recorded after its tests and commits. No remote issue is closed automatically.

## Issue map

| Planned ID | Issue title | Actual GitHub issue number | GitHub issue URL | Milestone | Priority | Dependencies | Current status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| [SA-001](issues/SA-001.md) | Bootstrap the runnable project | — | — | M1 | P0 | — | done-local |
| [SA-002](issues/SA-002.md) | Add migrations, persistent storage and repeatable reset | — | — | M1 | P0 | SA-001 | done-local |
| [SA-003](issues/SA-003.md) | Expand versioned synthetic application fixtures | — | — | M1 | P0 | SA-002 | in-progress |
| [SA-004](issues/SA-004.md) | Complete centralized typed tool metadata | — | — | M1 | P0 | SA-002 | in-progress |
| [SA-005](issues/SA-005.md) | Implement the complete synthetic file tool family | — | — | M1 | P0 | SA-003, SA-004 | in-progress |
| [SA-006](issues/SA-006.md) | Implement synthetic email tools and delivery records | — | — | M1 | P0 | SA-003, SA-004 | backlog |
| [SA-007](issues/SA-007.md) | Implement synthetic calendar tools and history | — | — | M1 | P0 | SA-003, SA-004 | backlog |
| [SA-008](issues/SA-008.md) | Introduce trusted sessions and confirmed task scopes | — | — | M2 | P0 | SA-002, SA-004 | in-progress |
| [SA-009](issues/SA-009.md) | Build deterministic mock and sandbox baseline modes | — | — | M2 | P0 | SA-005, SA-006, SA-007, SA-008 | in-progress |
| [SA-010](issues/SA-010.md) | Add configurable external model adapter | — | — | M2 | P1 | SA-004, SA-008 | backlog |
| [SA-011](issues/SA-011.md) | Implement bounded multi-step agent orchestration | — | — | M2 | P0 | SA-009, SA-010 | backlog |
| [SA-012](issues/SA-012.md) | Harden proposal validation and resolved targets | — | — | M3 | P0 | SA-004, SA-008 | in-progress |
| [SA-013](issues/SA-013.md) | Enforce operation and resource permissions | — | — | M3 | P0 | SA-008, SA-012 | in-progress |
| [SA-014](issues/SA-014.md) | Bind task authorization to concrete effects | — | — | M3 | P0 | SA-012, SA-013 | in-progress |
| [SA-015](issues/SA-015.md) | Enforce data sensitivity and recipient restrictions | — | — | M3 | P0 | SA-005, SA-006, SA-013, SA-014 | backlog |
| [SA-016](issues/SA-016.md) | Implement policy configuration and decision precedence | — | — | M3 | P0 | SA-013, SA-014, SA-015 | in-progress |
| [SA-017](issues/SA-017.md) | Consolidate the protected gateway and audit boundary | — | — | M3 | P0 | SA-011, SA-012, SA-016 | in-progress |
| [SA-018](issues/SA-018.md) | Complete adversarial authorization regression suite | — | — | M3 | P0 | SA-015, SA-016, SA-017 | in-progress |
| [SA-019](issues/SA-019.md) | Implement deterministic risk feature extraction | — | — | M4 | P1 | SA-017 | backlog |
| [SA-020](issues/SA-020.md) | Resolve consequential resource ambiguity | — | — | M4 | P0 | SA-019 | backlog |
| [SA-021](issues/SA-021.md) | Persist clarification requests and resume tasks | — | — | M4 | P0 | SA-008, SA-011, SA-020 | backlog |
| [SA-022](issues/SA-022.md) | Implement exact-action approval lifecycle | — | — | M4 | P0 | SA-015, SA-016, SA-017 | backlog |
| [SA-023](issues/SA-023.md) | Connect destructive and disclosure approval rules | — | — | M4 | P0 | SA-015, SA-022 | backlog |
| [SA-024](issues/SA-024.md) | Add sequence and dependency risk checks | — | — | M4 | P1 | SA-019, SA-021, SA-023 | backlog |
| [SA-025](issues/SA-025.md) | Evaluate risk decisions and interaction correctness | — | — | M4 | P1 | SA-020, SA-021, SA-022, SA-023, SA-024 | backlog |
| [SA-026](issues/SA-026.md) | Persist execution lifecycle and task ledger | — | — | M5 | P0 | SA-017 | in-progress |
| [SA-027](issues/SA-027.md) | Implement reproducible before-and-after fault injection | — | — | M5 | P0 | SA-006, SA-007, SA-026 | backlog |
| [SA-028](issues/SA-028.md) | Add persistent idempotency receipts | — | — | M5 | P0 | SA-006, SA-026 | backlog |
| [SA-029](issues/SA-029.md) | Implement bounded error-aware recovery | — | — | M5 | P0 | SA-027, SA-028 | backlog |
| [SA-030](issues/SA-030.md) | Reconcile unknown outcomes without blind retries | — | — | M5 | P0 | SA-028, SA-029 | backlog |
| [SA-031](issues/SA-031.md) | Enforce concurrent version and dependency safety | — | — | M5 | P0 | SA-024, SA-026, SA-029 | in-progress |
| [SA-032](issues/SA-032.md) | Complete recovery and partial-completion acceptance tests | — | — | M5 | P0 | SA-027, SA-028, SA-029, SA-030, SA-031 | backlog |
| [SA-033](issues/SA-033.md) | Define benchmark records and independent state judges | — | — | M6 | P0 | SA-009, SA-018, SA-025, SA-032 | backlog |
| [SA-034](issues/SA-034.md) | Build 200 grouped scenarios and frozen dataset splits | — | — | M6 | P1 | SA-033 | backlog |
| [SA-035](issues/SA-035.md) | Implement paired configurable experiment runner | — | — | M6 | P0 | SA-033, SA-034 | backlog |
| [SA-036](issues/SA-036.md) | Compute denominated metrics and statistical reports | — | — | M6 | P1 | SA-035 | backlog |
| [SA-037](issues/SA-037.md) | Evaluate prompt-injection families and model transfer | — | — | M6 | P1 | SA-010, SA-034, SA-035, SA-036 | backlog |
| [SA-038](issues/SA-038.md) | Train optional classical risk classifiers and calibration | — | — | M6 | P2 | SA-019, SA-034, SA-036 | backlog |
| [SA-039](issues/SA-039.md) | Add optional LLM risk evaluator and hybrid ablation | — | — | M6 | P2 | SA-010, SA-016, SA-019, SA-035, SA-038 | backlog |
| [SA-040](issues/SA-040.md) | Analyze failures and publish reproducible research artifacts | — | — | M6 | P1 | SA-036, SA-037, SA-038, SA-039 | backlog |
| [SA-041](issues/SA-041.md) | Build connected responsive playground and resource inspector | — | — | M7 | P1 | SA-008, SA-011, SA-017 | in-progress |
| [SA-042](issues/SA-042.md) | Add decision timeline, approvals and clarification UI | — | — | M7 | P1 | SA-021, SA-022, SA-026, SA-041 | in-progress |
| [SA-043](issues/SA-043.md) | Build paired baseline comparison and scenario explorer | — | — | M7 | P1 | SA-035, SA-037, SA-041 | backlog |
| [SA-044](issues/SA-044.md) | Implement measured evaluation analytics and export | — | — | M7 | P1 | SA-036, SA-040, SA-041 | backlog |
| [SA-045](issues/SA-045.md) | Add redacted audit filtering and complete browser acceptance | — | — | M7 | P1 | SA-026, SA-042, SA-043, SA-044 | backlog |
| [SA-046](issues/SA-046.md) | Complete related-work review and technical documentation | — | — | M8 | P1 | SA-018, SA-032, SA-040, SA-045 | in-progress |
| [SA-047](issues/SA-047.md) | Publish repository management and reproducible release workflow | — | — | M8 | P1 | SA-001, SA-046 | in-progress |
| [SA-048](issues/SA-048.md) | Verify eight demonstrations and final deliverable checklist | — | — | M8 | P0 | SA-040, SA-045, SA-046, SA-047 | backlog |

## Publication sequence

SA-001 and SA-002 have local acceptance evidence in commit `2884417`; `done-local` means verified and committed locally. It does not mean a remote issue was created or closed. All other tickets retain their partial/backlog status; no complete milestone is claimed.

1. Authenticate GitHub CLI and confirm the intended owner and repository.
2. Publish the local repository as `safeagent`, preserving commit history.
3. Create the eight milestones and labels from `backlog.json`; issue templates are already in `.github/ISSUE_TEMPLATE/`.
4. Create issues in planned-ID order using each prepared Markdown body and assign its milestone and labels.
5. Record GitHub-confirmed number and URL in the manifest; replace or augment planned dependencies with actual issue references.
6. Add native dependencies/sub-issues and the project board when supported. Never equate SA identifiers with GitHub numbers.

Types, priorities, components and statuses are defined in the manifest. The two additional component labels (`infrastructure`, `testing`) distinguish cross-cutting CI and acceptance work. Labels and milestones are prepared locally only.
