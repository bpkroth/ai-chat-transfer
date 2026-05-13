# Chat Bridge

A Python CLI tool to migrate chat history between various AI agents (Gemini, Claude, etc.).

## Features
- **Extractors:** Parse exports from Gemini (Google Takeout) and Claude (Anthropic JSON).
- **Injectors:** Output to high-fidelity Markdown (for "seeding" new chats) or common JSON.
- **Type-Safe:** Built with Pydantic and fully type-checked with **ty** (Rust-based).
- **Robust:** Modular architecture, unit-tested with Pytest.

## Installation

### Using `uv` (Recommended)
```bash
uv tool install .
```

### Using `pip`
```bash
pip install .
```

## Usage

### Migrate Gemini History to Markdown
```bash
chat-bridge migrate --from gemini --input takeout.json --to markdown --output summary.md
```

### Migrate Claude History to JSON
```bash
chat-bridge migrate --from claude --input claude_export.json --to json --output history.json
```

### Dry Run
```bash
chat-bridge migrate --from gemini --input takeout.json --dry-run
```

## Development

### Setup
```bash
uv sync
# Or using make (also installs pre-commit hooks)
make deps
```

### Pre-commit Hooks
Git hooks are automatically installed via `make deps`. To install them manually:
```bash
uv run pre-commit install
```

### Running Tests
```bash
uv run pytest
# Or using make
make test
```

### Linting, Formatting & Type Checking
```bash
# Individual commands
uv run ruff check .
uv run ruff format .
uv run ty check src
uv run pylint src/chat_bridge

# Run all checks via make
make check
```

### All-in-one
```bash
make all
```

## License
MIT
