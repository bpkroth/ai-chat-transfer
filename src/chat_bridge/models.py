from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field


class Message(BaseModel):
    """A single message in a chat history."""

    role: str = Field(
        ..., description="The role of the author (e.g., user, assistant, system)."
    )
    content: str = Field(..., description="The text content of the message.")
    timestamp: datetime | None = Field(
        None, description="The time the message was sent."
    )
    metadata: dict[str, Any] = Field(
        default_factory=dict, description="Additional agent-specific metadata."
    )


class ChatHistory(BaseModel):
    """A collection of messages representing a single chat session."""

    messages: list[Message]
    source: str = Field(..., description="The source agent (e.g., gemini, claude).")
    title: str | None = Field(None, description="Title of the chat session.")
    created_at: datetime | None = Field(None, description="When the chat was started.")
    metadata: dict[str, Any] = Field(
        default_factory=dict, description="Additional session-level metadata."
    )


class ExportData(BaseModel):
    """The top-level object for a multi-chat export."""

    chats: list[ChatHistory]
    exported_at: datetime = Field(default_factory=datetime.now)
    version: str = "1.0.0"
