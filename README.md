# Chat Bridge

A Python CLI tool to migrate chat history between various AI agents (Gemini, Claude, etc.).

## Features

- **Extractors:** Parse bulk exports or individual chat sessions from Gemini (Google Takeout) and Claude (Anthropic JSON).
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

### Migrate a Specific Chat Session

If your export contains many chats, you can migrate a single one by its title:

```bash
chat-bridge migrate --from gemini --input takeout.json --title "Project Alpha" --to markdown
```

> **Tip: Naming Sessions**
> Most agents allow you to explicitly name a session to make it easier to find:
>
> - **Gemini:** Click the three dots next to a chat in the sidebar and select **Rename**.
> - **Claude:** Click the chat title at the top of the screen to edit it, or use the sidebar menu.
> - **General:** If the agent supports it, sending a message like `/rename My New Title` sometimes works (agent dependent).

### Dry Run

```bash
chat-bridge migrate --from gemini --input takeout.json --dry-run
```

## Transferring Exports

If you need to move export files between machines (e.g., from a local download to a remote dev environment):

### Using SCP (Secure Copy)

```bash
# Copy export to a remote server
scp export.json user@remote-host:/path/to/destination/
```

### Using GitHub Gists

If you have the [GitHub CLI (`gh`)](https://cli.github.com/) installed, Gists are a convenient temporary buffer:

```bash
# Create a secret gist from your export
gh gist create export.json --public=false

# Download the gist on the target machine
gh gist view <gist-id> > export.json
```

## Contributing and Releases

See [CONTRIBUTING.md](./CONTRIBUTING.md) for development setup, checks, tests, and
PyPI release instructions.

## License

[MIT](./LICENSE)
