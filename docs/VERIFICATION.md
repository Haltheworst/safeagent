# Foundation verification log

Date: 2026-09-22. Local platform: Windows 11 (10.0.26200), Python 3.13.5, Node.js 24.11.0, npm 11.6.1, Git 2.48.1. All data used was synthetic.

## Executed checks

- Created an isolated virtual environment and installed `.[dev]` successfully after granting package-download network access.
- Installed frontend dependencies; npm reported zero known vulnerabilities at installation time. This is a point-in-time package audit, not a guarantee of security.
- Initial test collection failed because a parameter used Pytest's reserved name `request`; renamed it and reran.
- The subsequent suite passed 50 tests. After adding documentation/backlog checks and a pre-tool revalidation regression, the final complete suite passed **53 tests**, with two dependency deprecation warnings, in 18.90 seconds. This includes property examples and persistent-state checks.
- Final Ruff lint and formatting checks passed across the repository, including the protected runtime package.
- TypeScript checking and the Vite production build passed. The restricted environment initially prevented Vite's parent-path inspection; the build passed when run with required filesystem access.
- CLI database initialization, authorized demo, blocked adversarial mock demo, read task and inspection ran successfully. Successful renames changed FILE-001 title/version; blocked proposals did not modify FILE-002.
- API and Vite servers started on loopback ports 8000 and 5173. The frontend returned HTTP 200; live health and frontend-proxied summary requests succeeded with actual stored records.
- `python -m alembic check` reported no new upgrade operations. Explicit `reset --yes` restored fixture state and removed synthetic history.
- All local Markdown links and all 48 issue dependency/documentation references passed automated checks. A targeted credential-pattern scan found no matches. Git excludes the database, virtual environment, `.env`, installed frontend packages and build output, while retaining the source runtime package.

## Environment-specific failed combined run

`python scripts/dev.py check` was attempted with elevated permissions needed by Vite. Ruff passed, but Pytest's existing temporary/cache directories were owned by the sandbox account, so that combined invocation stopped with 44 fixture-setup permission errors and 9 passing tests. Running the full suite under its original sandbox identity passed all 53 tests; frontend type checking and production build passed separately under their required permissions. This environment-specific combined-command failure is not reported as a successful combined run. No test assertion failure was hidden or skipped.

## Limits and remaining verification

Connected browser inventory was empty and the in-app browser was unavailable, so visual/browser interaction acceptance and screenshots remain pending. This does not replace the completed frontend build and backend workflow tests. Unix instructions and the configured Windows/Linux CI matrix have not been executed on remote CI. No remote issue or repository publication has occurred. GitHub CLI authentication reported an invalid stored token.

The installed Starlette test client emits dependency deprecation warnings for httpx and the AnyIO blocking portal alias. Tests passed with these warnings; dependency compatibility should be reviewed during the next dependency update.

No paid model calls, research benchmark, external-service recovery experiment or ML evaluation was run. Local task history was reset during demonstrations and reset verification; deleted synthetic history is not retained, and fixtures are recoverable through reseeding.
