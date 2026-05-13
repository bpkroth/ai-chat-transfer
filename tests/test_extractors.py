"""Unit tests for the chat history extractors."""

import json

from chat_bridge.extractors.claude import ClaudeExtractor
from chat_bridge.extractors.gemini import GeminiExtractor


def test_gemini_extractor(tmp_path):
    """Test Gemini extractor with a list of chat objects."""
    d = tmp_path / "gemini.json"
    data = [
        {
            "title": "Test Chat",
            "messages": [
                {
                    "author": "user",
                    "content": "Hello",
                    "timestamp": "2024-05-12T10:00:00Z",
                },
                {
                    "author": "assistant",
                    "content": "Hi",
                    "timestamp": "2024-05-12T10:00:01Z",
                },
            ],
        }
    ]
    d.write_text(json.dumps(data))

    extractor = GeminiExtractor()
    export = extractor.extract(d)

    assert len(export.chats) == 1
    assert export.chats[0].title == "Test Chat"
    assert len(export.chats[0].messages) == 2
    assert export.chats[0].messages[0].role == "user"
    assert export.chats[0].messages[1].role == "assistant"


def test_claude_extractor(tmp_path):
    """Test Claude extractor with a list of chat objects."""
    d = tmp_path / "claude.json"
    data = [
        {
            "name": "Claude Chat",
            "created_at": "2024-05-12T11:00:00Z",
            "chat_messages": [
                {
                    "sender": "human",
                    "text": "Help",
                    "created_at": "2024-05-12T11:00:01Z",
                },
                {
                    "sender": "assistant",
                    "text": "Sure",
                    "created_at": "2024-05-12T11:00:02Z",
                },
            ],
        }
    ]
    d.write_text(json.dumps(data))

    extractor = ClaudeExtractor()
    export = extractor.extract(d)

    assert len(export.chats) == 1
    assert export.chats[0].title == "Claude Chat"
    assert len(export.chats[0].messages) == 2
    assert export.chats[0].messages[0].role == "user"
    assert export.chats[0].messages[1].role == "assistant"


def test_gemini_single_chat_extractor(tmp_path):
    """Test Gemini extractor with a single chat object."""
    d = tmp_path / "gemini_single.json"
    data = {
        "title": "Single Chat",
        "messages": [
            {"author": "user", "content": "One"},
            {"author": "assistant", "content": "Two"},
        ],
    }
    d.write_text(json.dumps(data))

    extractor = GeminiExtractor()
    export = extractor.extract(d)

    assert len(export.chats) == 1
    assert export.chats[0].title == "Single Chat"


def test_claude_single_chat_extractor(tmp_path):
    """Test Claude extractor with a single chat object."""
    d = tmp_path / "claude_single.json"
    data = {
        "name": "Single Claude",
        "chat_messages": [
            {"sender": "human", "text": "First"},
            {"sender": "assistant", "text": "Second"},
        ],
    }
    d.write_text(json.dumps(data))

    extractor = ClaudeExtractor()
    export = extractor.extract(d)

    assert len(export.chats) == 1
    assert export.chats[0].title == "Single Claude"
