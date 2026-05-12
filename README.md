# Chat Bridge

A well-crafted Python CLI tool to migrate chat history between various AI agents (Gemini, Claude, etc.).

## Features
- **Extractors:** Parse exports from Gemini (Google Takeout) and Claude (Anthropic JSON).
- **Injectors:** Output to high-fidelity Markdown (for "seeding" new chats) or common JSON.
- **Type-Safe:** Built with Pydantic and fully type-checked with Mypy.
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
```

### Running Tests
```bash
uv run pytest
```

### Linting & Formatting
```bash
uv run ruff check .
uv run mypy src
```

## License
MIT
