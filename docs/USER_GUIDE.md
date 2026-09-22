# Local demonstration guide

The playground supports exactly `Read FILE-001` and `Rename FILE-001 to <title>` (other syntactically valid FILE-nnn IDs are resolved and checked against ACLs). These are constrained direct-user commands, not general natural-language understanding. Unsupported requests display an error and create no task grant.

## Foundation demonstration

1. Open Sandbox explorer and note FILE-001's title/version and FILE-002's different owner.
2. Run the authorized demo card. It resets synthetic history, reads FILE-001, then renames it.
3. Inspect POLICY DECISION and EXECUTION VERIFICATION entries. Visit Sandbox explorer to confirm the changed title and incremented version.
4. Run the adversarial mock demo. Its deliberate scripted proposal tries to modify FILE-002 after the legitimate FILE-001 read. The trace shows BLOCK, and FILE-002 remains unchanged. This is a runtime test, not a real-model prompt-injection success-rate measurement.
5. Submit an unsupported task or try reading FILE-002 to see validation/permission failures.

The status report is generated from durable records and state checks. The UI awaits the backend's verified response. Trace rows expand into structured reason codes, arguments and observed state. Task counts are persisted local activity, never benchmark rates.

Reset removes synthetic tasks, execution/audit records and restores fixture files. UI reset requires confirmation; demo cards clearly disclose their reset behavior. Deleted traces are not recoverable unless you separately backed up the synthetic database; fixtures can always be regenerated.

The evaluation tab intentionally shows an empty/pending state. There are no approval or clarification forms yet. No mandatory full-project calendar, email timeout, disclosure, baseline comparison or benchmark demonstration is claimed complete.
