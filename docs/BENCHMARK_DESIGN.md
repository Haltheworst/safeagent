# Benchmark design — planned, not yet executed

Versioned benchmark target: at least 200 distinct scenarios: 40 normal tasks, 40 unauthorized/injection cases, 40 ambiguity cases, 40 recovery cases, 20 sensitive approval cases and 20 multi-step cases. Distribution may change with justification before freezing evaluation. The three current CLI demos are not this benchmark and do not count as 200 cases.

Each record will include scenario ID/category/description, initial fixture, trusted request, user permissions, attacker content, fault schedule, expected authorized behavior, forbidden effects, acceptable interactions, expected final state and completion predicates. Keep scenarios and judges separate from application policy code.

Group scenario families by task, payload mechanism and fixture similarity before assigning development, validation and held-out splits. Do not put a paraphrase of a training/development payload into the held-out split and call it novel. Freeze the held-out version, record later changes and do not tune policy using it.

Judge task completion and attacks using observable final state, not exact tool-call transcripts. A safe alternative execution path is acceptable. Count malicious proposals and executed side effects separately. Review state predicates for false positives and false negatives.

Faults must distinguish pre-execution and post-commit failure. Reinitialize equivalent state for paired configurations and repeated trials. Record scenario/policy/prompt versions, model/provider/parameters, seed, timestamp and source commit. Store raw JSONL or Parquet; summaries must be reproducible from raw records.

Scenario schema, generation, independent judges, runner and reports are SA-033–SA-040. They are unimplemented in v0.1.
