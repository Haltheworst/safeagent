# Installation and environment

The repository is intended to run from its root after an editable installation. Migrations and policy files are repository assets; a standalone distributable wheel is not yet supported. Use Python 3.12+ and Node.js 22.12+.

## Windows PowerShell

```powershell
py -3 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -e ".[dev]"
Copy-Item .env.example .env
.\.venv\Scripts\python.exe -m safeagent.cli init
npm.cmd --prefix frontend ci
.\.venv\Scripts\python.exe -m safeagent.cli serve
```

In a second terminal run `npm.cmd --prefix frontend run dev`. Explicit interpreter paths avoid changing the PowerShell execution policy. `npm.cmd` avoids the disabled `npm.ps1` wrapper.

## macOS and Linux

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -e '.[dev]'
cp .env.example .env
.venv/bin/python -m safeagent.cli init
npm --prefix frontend ci
.venv/bin/python -m safeagent.cli serve
```

In a second terminal run `npm --prefix frontend run dev`. Open <http://localhost:5173>; the API runs on <http://127.0.0.1:8000>. Basic local development does not require Docker. Cross-platform CI is configured; only Windows execution was locally verified in this session.

## Configuration

`SAFEAGENT_DATABASE_URL` defaults to `sqlite:///./runtime/safeagent.db`. Other database backends are rejected. `SAFEAGENT_POLICY_PATH` defaults to `config/default.json`; select `config/strict.json` for read-only policy. Missing or invalid policies fail startup rather than silently disabling enforcement.

No provider credentials are required or consumed by this release. `.env`, runtime databases, installed dependencies and build artifacts are Git-ignored. Installation needs package-registry network access once; ordinary tests need no live model or network service afterward.

Development environments with additional filesystem sandboxing may require permission for Vite to inspect parent paths while loading configuration. This was an execution-environment restriction during verification, not a requirement to change PowerShell security settings.
