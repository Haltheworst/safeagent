# Evaluation protocol — planned

The deterministic test suite checks runtime invariants. It does not measure a real LLM's susceptibility to injection or prove performance improvement over a baseline. No benchmark has run.

Planned configurations: BASELINE, POLICY_ONLY, POLICY_RISK, POLICY_RECOVERY, FULL_SAFEAGENT, OPTIONAL_ML and OPTIONAL_LLM_EVALUATOR. Keep model, prompt, task information and initial state equivalent across paired comparisons. The baseline must remain inside the synthetic simulator. Independently switch modules for controlled ablations.

## Metric definitions

| Metric | Numerator | Denominator |
| --- | --- | --- |
| Unauthorized execution | Scenarios with a forbidden effect | Scenarios with a forbidden-effect opportunity |
| Attack success | Attack scenarios achieving the objective | Evaluated attack scenarios |
| Unsafe interception | Genuinely unsafe proposals stopped before tool entry | Genuinely unsafe proposed actions |
| False block | Legitimate proposals incorrectly blocked | Legitimate proposals evaluated |
| Task completion | Legitimate tasks with verified correct completion | Legitimate tasks evaluated |
| Recovery success | Recoverable failures restored acceptably | Recoverable failure scenarios |
| Clarification precision | Necessary clarifications asked | All clarifications asked |
| Clarification recall | Necessary clarifications asked | Cases requiring clarification |
| Approval compliance | Approval-required executions with exact valid grants | Approval-required executions |

Zero denominators must be reported as undefined with counts, never silently as perfect performance. Also measure unintended target changes, duplicate effects, unauthorized disclosure counts, unknown handling, partial reporting, unnecessary approvals and interactions. State the applicable population for every rate.

Measure end-to-end and decision latency, actual tool/model calls, tokens and estimated cost with explicit provider price/version assumptions. Separate mock timing from live-model timing. Provide category breakdowns, confidence intervals and paired binary tests where appropriate. Statistical significance is not the same as practical importance.

Use a failure taxonomy including scope interpretation, policy configuration, resource resolution, stale authorization, approval binding, detector error, duplicate retry, unknown reconciliation and inaccurate reporting. Include false blocks and unnecessary questions. See [planned benchmark](BENCHMARK_DESIGN.md) and [results status](EXPERIMENTAL_RESULTS.md).
