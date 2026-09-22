# API reference — v0.1

Run the backend and open <http://127.0.0.1:8000/docs> for generated schemas. The API is a single-local-operator development interface, not authenticated multi-user hosting. Mutating endpoints require `X-SafeAgent-Client: local-ui`. Browser origins must match local port 5173 or 8000. The public marker is a browser request guard, not authentication.

| Method and route | Behavior |
| --- | --- |
| GET `/api/health` | Version and deterministic mock mode |
| GET `/api/tools` | Actual registered tool metadata and JSON schemas |
| POST `/api/tasks` | `{"request":"Read FILE-001"}`; run constrained task |
| GET `/api/tasks` | Most recent 100 stored tasks |
| GET `/api/tasks/{task_id}/trace` | Ordered persisted events, 404 for unknown task |
| POST `/api/demos` | `{"name":"authorized"}`, `blocked`, or `read`; reset then run |
| GET `/api/sandbox` | Operator-only synthetic file metadata |
| POST `/api/sandbox/reset` | `{"confirm":"RESET_SYNTHETIC_DATA"}`; delete synthetic history and reseed |
| GET `/api/summary` | Counts from local records; benchmark status remains NOT_IMPLEMENTED |

Unexpected request fields return 422. Unsupported command grammar returns 422. Unauthorized protected tool proposals return a structured BLOCK result inside the completed API request. Host/origin/header rejection returns 400/403. No endpoint accepts a user ID, permission grant, arbitrary tool call or model-generated approval.

Swagger POST requests also need the custom client header; use the connected UI or an HTTP client capable of adding it. Operator metadata and task inspection routes are never registered as agent tools.
