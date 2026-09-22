# Roadmap and local project board

This is the first functioning vertical slice, not a completed project. [48 provisional issue specifications](GITHUB_ISSUES.md) cover the full supplied requirements. Remote repository/board/issues are pending GitHub authentication.

| Milestone | Current state | Exit condition |
| --- | --- | --- |
| M1 — Foundation and Sandbox | In progress: read/rename file slice works | Versioned full file/email/calendar fixtures and tools pass tests |
| M2 — Functional LLM Agent | Partial deterministic two-step planner | External adapter, baseline and bounded general tool loop work |
| M3 — Runtime Policy Enforcement | Basic task/resource/effect/version checks work | Full recipient/disclosure and multi-domain security matrix passes |
| M4 — Risk Detection and Approvals | Planned | Clarification, exact approvals and deterministic risk workflows pass |
| M5 — Execution Monitoring and Recovery | Durable local execution slice works | Fault schedule, idempotency, unknown reconciliation and bounded recovery pass |
| M6 — Research Evaluation | Planned | 200 grouped scenarios, paired ablations and measured reports exist |
| M7 — Dashboard and Demonstration | Connected foundation UI works | Full interactive workflows, comparisons, charts and audit export pass |
| M8 — Documentation and Release | Initial documentation/backlog prepared | All demonstrations, documentation, publication and release checks pass |

## Next dependency-ready issue

SA-003: expand versioned synthetic fixtures for contacts, emails, calendar events and folder/file cases. Then complete SA-004 tool metadata coverage and SA-005–SA-007 application tools before the full model/baseline loop. Keep this foundation executable throughout.

## Board interpretation

Backlog: not started. Ready: dependencies verified. In Progress: implementation or acceptance checks incomplete. In Review: complete local evidence awaiting review. Done: all acceptance criteria verified and committed. No milestone is marked complete merely because modules or schemas exist.

Future contributions should work on one coherent slice, update issue evidence and documentation, then commit. Optional ML and semantic risk evaluation follow deterministic coverage and benchmark design.
