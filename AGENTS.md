# AI Agents Instructions

This repository contains tools for migrating chat history between various AI agents.

## Core Mandates
- **Context Preservation:** When migrating, prioritize preserving the semantic context of the conversation.
- **Privacy:** Never include sensitive information, API keys, or personal credentials in exported chat histories.
- **Formatting:** Standardize on OpenAI-compatible JSON for internal representation and Markdown for human-readable summaries.

## Supported Agents
- **Gemini:** Use Google Takeout to export JSON history.
- **Claude:** Use the built-in "Export Data" feature to get JSON history.
- **Codex/Copilot:** (Research in progress for local storage locations).

## Migration Workflow
1. Export history from the source agent as JSON.
2. Run `chat-bridge migrate --from <source> --input <file> --to markdown`.
3. Copy the resulting Markdown summary.
4. Paste the summary into a new chat with the target agent to "seed" the context.

## Local Conventions
- All Python code must pass `make check` (Ruff, Pylint, Ty) with a 10.0/10 score.
  - Use pre-commit hooks to check for that.
- Unit tests are required for all new extractors and injectors.
