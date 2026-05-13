"""Extractor for Claude chat history."""

import json
from contextlib import suppress
from datetime import datetime
from pathlib import Path

from chat_bridge.core import BaseExtractor
from chat_bridge.models import ChatHistory, ExportData, Message


class ClaudeExtractor(BaseExtractor):
    """Extractor for Claude JSON export files."""

    def extract(self, input_path: Path) -> ExportData:
        """Extract chat history from a Claude JSON file."""
        with input_path.open(encoding="utf-8") as f:
            raw_data = json.load(f)

        chats = []
        # Claude exports are typically a list of conversation objects,
        # but handle a single conversation object as well.
        if isinstance(raw_data, dict):
            conversations = [raw_data]
        elif isinstance(raw_data, list):
            conversations = raw_data
        else:
            raise ValueError(f"Unexpected Claude data format: {type(raw_data)}")

        for conv in conversations:
            messages = []
            for msg in conv.get("chat_messages", []):
                role = "user" if msg.get("sender") == "human" else "assistant"
                content = msg.get("text", "")

                ts = None
                if "created_at" in msg:
                    with suppress(ValueError):
                        ts = datetime.fromisoformat(
                            msg["created_at"].replace("Z", "+00:00")
                        )

                messages.append(
                    Message(role=role, content=content, timestamp=ts, metadata=msg)
                )

            created_at = None
            if "created_at" in conv:
                with suppress(ValueError):
                    created_at = datetime.fromisoformat(
                        conv["created_at"].replace("Z", "+00:00")
                    )

            chats.append(
                ChatHistory(
                    messages=messages,
                    source="claude",
                    title=conv.get("name"),
                    created_at=created_at,
                    metadata=conv,
                )
            )

        return ExportData(chats=chats)
