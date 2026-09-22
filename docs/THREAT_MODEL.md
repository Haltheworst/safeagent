# Threat model

## Protected assets and objectives

The initial protected assets are synthetic file titles/content, ownership permissions, task scope, execution records and truthful completion reports. The objective is to prevent model-proposed reads or mutations outside the trusted task and resource permissions, and to avoid claiming a mutation succeeded without observable evidence.

## Attacker capabilities

The attacker may influence a retrieved document body, model-proposed tool name, arguments, explanation, evidence references and claimed permission. The attacker may try role spoofing, fake approvals, alternate target identifiers, injected code strings or repeated requests. `FILE-003` contains a visible authority-spoofing payload. The adversarial mock demo scripts a forbidden proposal explicitly; it does not measure whether an LLM follows that payload.

The attacker cannot modify direct trusted user requests, server policy, stored task grants, resource ACLs, application code or trusted identity. The model has no general-purpose shell, HTTP, filesystem or database tool.

## Trust assumptions

The local operator, server process, database, Python imports, dependency supply chain and OS are trusted. Process-local Python interfaces are architectural boundaries, not security isolation against arbitrary malicious Python. The loopback operator API has no real authentication and must not be exposed to other users. Host/origin checks and a custom client header mitigate browser-origin mistakes; the header is public and is not an authentication credential.

## Covered foundation behavior

Strict schemas reject unexpected authority flags and unknown operations. Both reads and mutations check task and ACL permissions. Exact title binding prevents effect substitution. Version checking rejects stale mutations. Refusal tests inspect final state and tool-attempt counters.

## Outside coverage and residual risks

General natural-language intent interpretation, data lineage through summaries, authorized-looking harmful content, external disclosure, compromised trusted components, distributed failures and real service semantics are not solved. A malicious payload that changes an already authorized title to the exact user-approved value is indistinguishable at this boundary. Incorrect user scopes or policy configuration can authorize harmful behavior. Retrieved text may still manipulate an eventual model response without causing a protected tool mutation.

The planned attack benchmark includes exfiltration, calendar manipulation, deletion, role spoofing, approval spoofing, tool-output laundering, multi-step manipulation and encoded/obfuscated variations. Blocking one scripted proposal is not evidence that prompt injection is eliminated.
