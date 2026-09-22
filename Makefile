.PHONY: install init test lint frontend check serve
PYTHON ?= python
install:
	$(PYTHON) -m pip install -e ".[dev]"
	npm --prefix frontend ci
init:
	$(PYTHON) -m safeagent.cli init
test:
	$(PYTHON) -m pytest
lint:
	$(PYTHON) -m ruff check .
	$(PYTHON) -m ruff format --check .
frontend:
	npm --prefix frontend run build
check:
	$(PYTHON) scripts/dev.py check
serve:
	$(PYTHON) -m safeagent.cli serve
