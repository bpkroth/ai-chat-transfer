.PHONY: all check test package clean install help

# Default target
all: check test

help:
	@echo "Usage: make [target]"
	@echo ""
	@echo "Targets:"
	@echo "  deps      Install dependencies using uv"
	@echo "  check     Run linting (ruff, pylint) and type checking (ty)"
	@echo "  test      Run unit tests (pytest)"
	@echo "  package   Build the wheel and source distribution"
	@echo "  install   Install the tool locally using uv"
	@echo "  clean     Remove build artifacts and cache files"
	@echo "  all       Run check and test"

deps:
	uv sync

check:
	uv run ruff check .
	uv run ruff format --check .
	uv run pylint src/chat_bridge
	uv run ty check src

test:
	uv run pytest

package:
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
