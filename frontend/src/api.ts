export interface Summary {
  tasks: number; completed_tasks: number; verified_executions: number;
  blocked_proposals: number; tool_attempts: number; evaluated_tasks: number;
}
export interface FileRow {
  id: string; title: string; owner_id: string; sensitivity: string; version: number;
}
export interface Task {
  task_id: string; request: string; status: string; report: string; created_at: string;
}
export interface Trace {
  id: number; kind: string; action_id: string | null;
  details: Record<string, unknown>; timestamp: string;
}
export interface TaskResult { task_id: string; status: string; report: string; }

export async function api<T>(path: string, body?: unknown): Promise<T> {
  const response = await fetch(`/api${path}`, {
    method: body === undefined ? "GET" : "POST",
    headers: { "Content-Type": "application/json", "X-SafeAgent-Client": "local-ui" },
    body: body === undefined ? undefined : JSON.stringify(body),
  });
  if (!response.ok) {
    const error: unknown = await response.json().catch(() => null);
    const detail = error && typeof error === "object" && "detail" in error ? error.detail : null;
    throw new Error(typeof detail === "string" ? detail : `API request failed (${response.status}).`);
  }
  return response.json() as Promise<T>;
}
