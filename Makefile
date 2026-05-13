.PHONY: all check test package clean install help

# Default target
all: check test

help:
	@echo "Usage: make [target]"
	@echo ""
	@echo "Targets:"
	@echo "  deps      Install dependencies and pre-commit hooks using uv"
	@echo "  check     Run pre-commit checks against all files"
	@echo "  test      Run unit tests (pytest)"
	@echo "  package   Build the wheel and source distribution"
	@echo "  install   Install the tool locally using uv"
	@echo "  clean     Remove build artifacts and cache files"
	@echo "  all       Run check and test"

deps:
	uv python install
	uv sync
	uv run pre-commit install

check: deps
	uv run pre-commit run -a

test: deps
	uv run pytest

package: deps
	uv build

install:
	uv tool install . --force

clean:
	rm -rf dist/
	rm -rf build/
	rm -rf *.egg-info
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	find . -type d -name ".ruff_cache" -exec rm -rf {} +
