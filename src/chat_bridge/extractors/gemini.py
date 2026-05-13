"""Extractor for Gemini chat history."""

import json
from contextlib import suppress
from datetime import datetime
from pathlib import Path

from chat_bridge.core import BaseExtractor
from chat_bridge.models import ChatHistory, ExportData, Message


class GeminiExtractor(BaseExtractor):
    """Extractor for Gemini Google Takeout files."""

    def extract(self, input_path: Path) -> ExportData:
        """Extract chat history from a Gemini JSON file."""
        with input_path.open(encoding="utf-8") as f:
            raw_data = json.load(f)

        chats = []
        # Google Takeout for Gemini is often a list of chat objects
        # Structure varies, but usually it's a list or a dict with a 'conversations' key
        if isinstance(raw_data, list):
            conversations = raw_data
        else:
            conversations = raw_data.get("conversations", [])

        for conv in conversations:
            messages = []
            for msg in conv.get("messages", []):
                role = "user" if msg.get("author") == "user" else "assistant"
                content = msg.get("content", "")

                # Try to parse timestamp
                ts = None
                if "timestamp" in msg:
                    with suppress(ValueError):
                        ts = datetime.fromisoformat(
                            msg["timestamp"].replace("Z", "+00:00")
                        )

                messages.append(
                    Message(role=role, content=content, timestamp=ts, metadata=msg)
                )

            chats.append(
                ChatHistory(
                    messages=messages,
                    source="gemini",
                    title=conv.get("title"),
                    created_at=None,
                    metadata=conv,
                )
            )

        return ExportData(chats=chats)
