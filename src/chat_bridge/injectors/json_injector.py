"""Injector for JSON format."""

import sys
from pathlib import Path

from chat_bridge.core import BaseInjector
from chat_bridge.models import ExportData

DRY_RUN_PREVIEW_LIMIT = 500


class JsonInjector(BaseInjector):
    """Injector that serializes chat history to JSON."""

    def inject(self, data: ExportData, output_path: Path | None, dry_run: bool) -> None:
        """Inject chat history into a JSON file or stdout."""
        # Use Pydantic's model_dump_json for clean serialization
        json_text = data.model_dump_json(indent=2)

        if dry_run:
            print("--- DRY RUN: JSON Output ---")
            if len(json_text) > DRY_RUN_PREVIEW_LIMIT:
                print(f"{json_text[:DRY_RUN_PREVIEW_LIMIT]}...")
            else:
                print(json_text)
            return

        if output_path:
            with output_path.open("w", encoding="utf-8") as f:
                f.write(json_text)
        else:
            sys.stdout.write(json_text)
