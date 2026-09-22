# Contributing

Start with [the local issue map](docs/GITHUB_ISSUES.md) and read the linked issue specification. Do not assume an SA identifier is a GitHub issue number. Remote publication is pending.

Use `feat/`, `fix/`, `docs/`, or `test/` branches for a coherent change. Preserve the gateway boundary: no direct application tool calls from agent code, no model-controlled authorization fields, and no real accounts. Add observed-state regression tests for every security or recovery change. Run `python scripts/dev.py check` in the installed development environment before proposing a change.

Use conventional commit messages. Pull requests should explain the behavior, relevant threat assumptions, verification evidence, and documentation changes. Link dependencies and never close an issue until all acceptance criteria are met. Do not claim model evaluations were run when only deterministic runtime tests passed.

Do not commit secrets, `.env`, runtime databases, virtual environments, or unsanitized execution data. Keep demo fixtures synthetic. See [SECURITY.md](SECURITY.md).
