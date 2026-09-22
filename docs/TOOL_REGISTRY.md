# Tool registry

`GET /api/tools` exposes actual registry metadata and JSON schemas. Agent code dispatches only through the gateway; it never dynamically executes supplied code. Tool metadata is defined in `src/safeagent/sandbox/tools.py`.

| Tool | Arguments | Permission | Effects | Verification | Retry metadata |
| --- | --- | --- | --- | --- | --- |
| `read_file` | `file_id` | READ_FILE | Read synthetic content | Resource and response equality | SAFE_RETRY |
| `update_file` | `file_id`, `changes.title`, `expected_version` | WRITE_FILE | Title change and version increment | Actual title and incremented version | VERIFY_BEFORE_RETRY |

Both tools use exact FILE-nnn identifiers and reject extra arguments. The update surface is title-only, not arbitrary content mutation. Neither operation sends data to real accounts. Registry metadata declares resource type, read-only status, external effect, reversibility, natural idempotence, key support, approval requirement, response schema, verifier and retry strategy. Neither currently supports a native idempotency key; metadata is not a claim that the recovery controller already exists.

Read output includes untrusted provenance and content. Execution/audit receipts omit content. Reads require the same independent authorization boundary as writes.

Other file, email and calendar tools from the specification are pending SA-005–SA-007. They are not advertised or accepted as executable tools.
