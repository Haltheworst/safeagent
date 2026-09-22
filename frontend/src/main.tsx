import { StrictMode, useEffect, useRef, useState } from "react";
import { createRoot } from "react-dom/client";
import { api, type FileRow, type Summary, type Task, type TaskResult, type Trace } from "./api";
import "./style.css";

function App() {
  const [view, setView] = useState<"playground" | "sandbox" | "research">("playground");
  const [summary, setSummary] = useState<Summary | null>(null);
  const [files, setFiles] = useState<FileRow[]>([]);
  const [tasks, setTasks] = useState<Task[]>([]);
  const [trace, setTrace] = useState<Trace[]>([]);
  const [selected, setSelected] = useState("");
  const [request, setRequest] = useState("Rename FILE-001 to Reviewed project report");
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");
  const [result, setResult] = useState<TaskResult | null>(null);
  const traceRequest = useRef(0);

  async function refresh() {
    const [s, f, t] = await Promise.all([
      api<Summary>("/summary"), api<{ files: FileRow[] }>("/sandbox"), api<Task[]>("/tasks"),
    ]);
    setSummary(s); setFiles(f.files); setTasks(t);
  }
  useEffect(() => { refresh().catch((e: Error) => setError(e.message)); }, []);

  async function inspect(taskId: string) {
    const generation = ++traceRequest.current;
    setSelected(taskId); setTrace([]);
    try {
      const events = await api<Trace[]>(`/tasks/${encodeURIComponent(taskId)}/trace`);
      if (traceRequest.current === generation) setTrace(events);
    } catch (e) { if (traceRequest.current === generation) setError((e as Error).message); }
  }

  async function run(demo?: string) {
    setBusy(true); setError(""); setResult(null);
    try {
      const response = await api<TaskResult>(demo ? "/demos" : "/tasks", demo ? { name: demo } : { request });
      setResult(response); await refresh(); await inspect(response.task_id);
    } catch (e) { setError((e as Error).message); }
    finally { setBusy(false); }
  }

  async function reset() {
    if (!window.confirm("Reset synthetic files and permanently remove local task and execution history?")) return;
    setBusy(true); setError("");
    try {
      await api("/sandbox/reset", { confirm: "RESET_SYNTHETIC_DATA" });
      ++traceRequest.current; setTrace([]); setSelected(""); setResult(null); await refresh();
    } catch (e) { setError((e as Error).message); }
    finally { setBusy(false); }
  }

  return <div className="app-shell">
    <aside className="sidebar">
      <a className="brand" href="#"><span className="brand-mark">S</span>SafeAgent<span className="version">0.1</span></a>
      <div className="workspace-label">RUNTIME LABORATORY</div>
      <nav aria-label="Main navigation">
        {(["playground", "sandbox", "research"] as const).map((item, index) => <button key={item}
          className={view === item ? "nav-item active" : "nav-item"} onClick={() => setView(item)}>
          <span className="nav-number">0{index + 1}</span>{item === "playground" ? "Agent playground" : item === "sandbox" ? "Sandbox explorer" : "Evaluation"}
        </button>)}
      </nav>
      <div className="boundary-note"><span className="status-dot" />Local synthetic environment
        <p>Every agent read and mutation passes through the protected gateway.</p>
      </div>
      <div className="sidebar-bottom">FOUNDATION RELEASE<br /><span>Deterministic mock agent</span></div>
    </aside>
    <main>
      <header className="topbar"><span>Workspace <span className="separator">/</span> {view}</span>
        <button className="button quiet" disabled={busy} onClick={reset}>Reset sandbox</button></header>
      <div className="main-content">
        <div className="page-heading"><div><div className="eyebrow">PROPOSALS → POLICIES → VERIFIED EFFECTS</div>
          <h1>{view === "playground" ? "Observe the safety boundary." : view === "sandbox" ? "Inspect the actual state." : "Evidence before claims."}</h1>
          <p>{view === "playground" ? "Follow what the agent proposed, what was allowed, and what actually changed." : view === "sandbox" ? "Synthetic resources, ownership, and versions from the local database." : "Research metrics will appear after the benchmark runner is implemented."}</p></div>
          <span className="tag">MOCK MODE</span></div>
        {error && <div className="error-box" role="alert">{error} <button onClick={() => { setError(""); refresh().catch((e: Error) => setError(e.message)); }}>Retry connection</button></div>}
        <section className="stats" aria-label="Stored local activity">
          {[["Local tasks", summary?.tasks], ["Verified completions", summary?.completed_tasks], ["Blocked proposals", summary?.blocked_proposals], ["Tool attempts", summary?.tool_attempts]].map(([label, value]) =>
            <article className="stat" key={label}><span>{label}</span><strong>{value ?? "—"}</strong><small>Stored local activity</small></article>)}
        </section>
        {view === "playground" && <>
          <section className="panel composer"><div className="section-title"><h2>Give the agent a task</h2><span className="small-label">EXACT COMMAND MODE</span></div>
            <form onSubmit={(e) => { e.preventDefault(); void run(); }}><label htmlFor="request">Trusted user request</label>
              <textarea id="request" value={request} onChange={(e) => setRequest(e.target.value)} maxLength={500} disabled={busy} rows={2} />
              <div className="composer-bottom"><p>Try <code>Read FILE-001</code> or <code>Rename FILE-001 to My title</code></p><button className="button primary" disabled={busy || !request.trim()}>{busy ? "Executing and verifying…" : "Run task →"}</button></div>
            </form>
          </section>
          <div className="demo-grid">
            <button className="demo-card" disabled={busy} onClick={() => void run("authorized")}><span className="demo-code">01 / AUTHORIZED</span><strong>Read, then rename <span>↗</span></strong><p>A permitted two-step workflow with a verified state change.</p></button>
            <button className="demo-card" disabled={busy} onClick={() => void run("blocked")}><span className="demo-code">02 / ADVERSARIAL MOCK</span><strong>Cross the boundary <span>↗</span></strong><p>A scripted unauthorized proposal tests resource and task permissions.</p></button>
          </div><p className="demo-note">Demo cards reset synthetic files and task history before running. They do not call an external LLM.</p>
          {result && <section className={`result-box ${result.status === "COMPLETED" ? "success" : "warning"}`} aria-live="polite"><span className="badge">{result.status}</span><p>{result.report}</p></section>}
          <section className="panel"><div className="section-title"><h2>Execution timeline</h2><span className="small-label">PERSISTED EVENTS</span></div>
            <label className="sr-only" htmlFor="task">Choose task</label><select id="task" value={selected} disabled={busy} onChange={(e) => void inspect(e.target.value)}><option value="" disabled>Select a stored task</option>{tasks.map(t => <option value={t.task_id} key={t.task_id}>{t.request} · {t.status} · {t.task_id.slice(0, 8)}</option>)}</select>
            {trace.length === 0 ? <div className="empty-state"><div className="empty-symbol">⌁</div><h3>No trace selected</h3><p>Run a task to inspect its proposals, decisions, and verified outcomes.</p></div> : <ol className="timeline">{trace.map((event) => <li key={event.id}>
              <span className={`timeline-dot ${event.details.decision === "BLOCK" ? "blocked" : ""}`} />
              <details><summary><span>{event.kind.replaceAll("_", " ")}</span><span className="event-decision">{String(event.details.decision ?? "")}</span><time>{event.timestamp.slice(11, 19)}</time></summary>
                {typeof event.details.human_readable_explanation === "string" && <p>{event.details.human_readable_explanation}</p>}<pre>{JSON.stringify(event.details, null, 2)}</pre>
              </details></li>)}</ol>}
          </section>
        </>}
        {view === "sandbox" && <section className="panel"><div className="section-title"><h2>File resources</h2><span className="small-label">FIXTURE foundation-1</span></div><p className="muted">Operator inspection only. This view is not available as an agent tool.</p>
          <div className="table-scroll"><table><thead><tr><th>Resource</th><th>Title</th><th>Owner</th><th>Sensitivity</th><th>Version</th></tr></thead><tbody>{files.map(file => <tr key={file.id}><td><code>{file.id}</code></td><td>{file.title}</td><td>{file.owner_id}</td><td><span className="badge">{file.sensitivity}</span></td><td>v{file.version}</td></tr>)}</tbody></table></div>
        </section>}
        {view === "research" && <section className="panel research-empty"><span className="tag">EXPERIMENTS PENDING</span><h2>No research results yet.</h2><p>The foundation has local demonstration traces. A versioned benchmark, baseline comparisons, grouped dataset splits, recovery experiments, and statistical reports are planned in milestone M6.</p><p>Local completion counts do not establish safety efficacy or generalization to real models.</p><div className="research-target"><span>Development target</span><strong>200 scenarios</strong><span>0 benchmark trials recorded</span></div></section>}
        <footer>SafeAgent · Runtime safety & reliability <span>Single local operator · Synthetic data only</span></footer>
      </div>
    </main>
  </div>;
}

createRoot(document.getElementById("root")!).render(<StrictMode><App /></StrictMode>);
