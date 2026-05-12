import sys
from pathlib import Path

from chat_bridge.core import BaseInjector
from chat_bridge.models import ExportData


class MarkdownInjector(BaseInjector):
    def inject(self, data: ExportData, output_path: Path | None, dry_run: bool) -> None:
        output = []
        output.append("# Chat History Summary\n")
        output.append(f"Exported at: {data.exported_at}\n")

        for i, chat in enumerate(data.chats):
            output.append(f"## Chat {i + 1}: {chat.title or 'Untitled'}")
            output.append(f"Source: {chat.source}\n")

            for msg in chat.messages:
                role_label = "**User**" if msg.role == "user" else "**Assistant**"
                output.append(f"{role_label}: {msg.content}\n")

            output.append("---\n")

        final_text = "\n".join(output)

        if dry_run:
            print("--- DRY RUN: Markdown Output ---")
            print(final_text[:500] + "..." if len(final_text) > 500 else final_text)
            return

        if output_path:
            with output_path.open("w", encoding="utf-8") as f:
                f.write(final_text)
        else:
            sys.stdout.write(final_text)
