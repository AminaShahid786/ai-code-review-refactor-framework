# -----------------------------------------------------------------------------
# Makefile — Phase 2 (Development Environment & Tooling)
#
# Only targets meaningful at this phase are defined here. Later phases
# (docker-compose targets in Phase 3, `make migrate` in Phase 5, etc.) will
# extend this file — not before.
# -----------------------------------------------------------------------------

.DEFAULT_GOAL := help
VENV_DIR := .venv
PYTHON := python3
VENV_PY := $(VENV_DIR)/bin/python
VENV_PIP := $(VENV_DIR)/bin/pip

.PHONY: help setup venv install-dev precommit-install env lint format typecheck test check clean

help: ## Show this help message
	@echo "Available targets:"
	@awk 'BEGIN {FS = ":.*##"} /^[a-zA-Z_-]+:.*##/ {printf "  \033[36m%-18s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

setup: venv install-dev precommit-install env ## Bootstrap a complete local dev environment (one command)
	@echo ""
	@echo "Setup complete."
	@echo "Activate the virtual environment with: source $(VENV_DIR)/bin/activate"

venv: ## Create the Python virtual environment if it doesn't exist
	@if [ ! -d "$(VENV_DIR)" ]; then \
		echo "Creating virtual environment in $(VENV_DIR)..."; \
		$(PYTHON) -m venv $(VENV_DIR); \
	else \
		echo "Virtual environment already exists at $(VENV_DIR)."; \
	fi

install-dev: venv ## Install development dependencies (Ruff, Black, Mypy, pre-commit, pytest)
	$(VENV_PIP) install --upgrade pip
	$(VENV_PIP) install -e ".[dev]"

precommit-install: venv ## Install git pre-commit hooks
	$(VENV_DIR)/bin/pre-commit install

env: ## Create a local .env from .env.example if one doesn't already exist
	@if [ ! -f ".env" ]; then \
		cp .env.example .env; \
		echo "Created .env from .env.example."; \
	else \
		echo ".env already exists — leaving it untouched."; \
	fi

lint: ## Run Ruff lint checks (no fixes applied)
	$(VENV_DIR)/bin/ruff check .

format: ## Auto-format the codebase with Ruff and Black
	$(VENV_DIR)/bin/ruff format .
	$(VENV_DIR)/bin/black .

typecheck: ## Run Mypy static type checking
	$(VENV_DIR)/bin/mypy .

test: ## Run the test suite. Treats "no tests collected yet" (pytest exit code 5) as success.
	@$(VENV_DIR)/bin/pytest; \
	status=$$?; \
	if [ $$status -eq 0 ] || [ $$status -eq 5 ]; then \
		echo "pytest completed (exit $$status: $$( [ $$status -eq 5 ] && echo 'no tests collected yet, expected at this phase' || echo 'all tests passed' ))."; \
		exit 0; \
	else \
		exit $$status; \
	fi

check: lint typecheck test ## Run lint, typecheck, and test together (mirrors CI, once CI exists)

precommit-all: ## Run all pre-commit hooks against every file in the repo
	$(VENV_DIR)/bin/pre-commit run --all-files

clean: ## Remove the virtual environment and tool caches
	rm -rf $(VENV_DIR) .pytest_cache .ruff_cache .mypy_cache
	find . -type d -name "__pycache__" -not -path "./node_modules/*" -exec rm -rf {} +
