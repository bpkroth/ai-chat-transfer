import sys
from pathlib import Path

from chat_bridge.core import BaseInjector
from chat_bridge.models import ExportData


class JsonInjector(BaseInjector):
    def inject(self, data: ExportData, output_path: Path | None, dry_run: bool) -> None:
        # Use Pydantic's model_dump_json for clean serialization
        json_text = data.model_dump_json(indent=2)

        if dry_run:
            print("--- DRY RUN: JSON Output ---")
            print(json_text[:500] + "..." if len(json_text) > 500 else json_text)
            return

        if output_path:
            with output_path.open("w", encoding="utf-8") as f:
                f.write(json_text)
        else:
            sys.stdout.write(json_text)
