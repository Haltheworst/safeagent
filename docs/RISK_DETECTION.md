# Risk detection

Foundation behavior includes deterministic resource existence, task/effect scope, ACL and resource-version checks. Their explanations are surfaced in the trace. These rules are implemented in the policy engine; a separate replaceable detector is planned in SA-019.

The full risk vocabulary will distinguish resource ambiguity, missing information, unverified target, external disclosure, destructive action, injection indicator, unexpected sequence, duplicate risk, stale state, unmet dependency and unknown outcome. They do not all map to the same response. A mandatory permission denial cannot be replaced by clarification, and clarification does not create a missing ACL grant.

Ambiguity detection must use trusted exact selections and available context rather than search-result count alone. Clarification must bind a real user answer to a resource before reevaluation. These workflows are not yet implemented; unsupported commands currently receive a validation error.

## Planned learned and semantic methods

After deterministic coverage, compare logistic regression and random forest using versioned structured features. Labels are EXECUTE_CANDIDATE, CLARIFICATION_NEEDED, APPROVAL_RECOMMENDED and BLOCK_RECOMMENDED. Recommendations may restrict or request review; they may never override a deterministic denial.

Rule-generated labels are development data, not independent evidence of generalization. Reserve a manually labeled evaluation subset for actual independent human review; the assistant cannot claim to supply independent human judgment. Report class balance, confusion matrices, category errors, calibration/Brier score and uncertain recommendations.

An optional LLM evaluator will receive clearly separated trusted task/policy metadata and untrusted retrieved content. It gets no credentials or executable tools. Compare deterministic-only, deterministic+ML, deterministic+LLM and hybrid settings with paired inputs. Record latency, token usage and explicit price assumptions. No learned model or semantic evaluator is shipped or evaluated in v0.1.
