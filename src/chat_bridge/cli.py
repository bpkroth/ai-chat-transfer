"""Command line interface for the chat-bridge tool."""

import sys

import click

from chat_bridge.core import Bridge


@click.group()
@click.version_option()
def main() -> None:
    """Chat Bridge: Migrate chat history between AI agents."""


@main.command()
@click.option(
    "--from", "source", required=True, help="Source agent (e.g., gemini, claude)."
)
@click.option(
    "--input",
    "input_file",
    required=True,
    type=click.Path(exists=True),
    help="Input export file.",
)
@click.option(
    "--output", "output_file", type=click.Path(), help="Output file (default: stdout)."
)
@click.option(
    "--to", "target", default="markdown", help="Target format (e.g., markdown, json)."
)
@click.option(
    "--title",
    help=(
        "Filter for a specific chat session by title. "
        "Use agent commands (like /rename) to set titles before exporting."
    ),
)
@click.option(
    "--dry-run", is_flag=True, help="Show what would be done without writing."
)
def migrate(  # pylint: disable=too-many-arguments
    source: str,
    input_file: str,
    output_file: str | None,
    target: str,
    title: str | None,
    dry_run: bool,
) -> None:
    """Migrate chat history from one agent to another."""
    bridge = Bridge(dry_run=dry_run)
    try:
        bridge.run(source, input_file, target, output_file, title=title)
    except (ValueError, FileNotFoundError, PermissionError) as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)
    except Exception as e:  # pylint: disable=broad-exception-caught
        click.echo(f"An unexpected error occurred: {e}", err=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
