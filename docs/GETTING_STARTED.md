# Getting started

Follow [installation](INSTALLATION.md), then run the two deterministic demonstrations:

```sh
python -m safeagent.cli demo authorized
python -m safeagent.cli demo blocked
```

Use the virtual-environment interpreter path shown in installation if it is not activated. Each demo resets only local synthetic data and history. The first verifies a permitted FILE-001 rename; the second explicitly scripts an unauthorized mutation after a permitted read. Inspect returned decisions and run `python -m safeagent.cli inspect` to see actual state.

For non-resetting tasks, run `python -m safeagent.cli run "Read FILE-001"`. Start the API and frontend to inspect the same persisted data. See [user guide](USER_GUIDE.md) for interface behavior and limitations.
