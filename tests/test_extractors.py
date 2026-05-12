import json
from pathlib import Path
from chat_bridge.extractors.gemini import GeminiExtractor
from chat_bridge.extractors.claude import ClaudeExtractor

def test_gemini_extractor(tmp_path):
    d = tmp_path / "gemini.json"
    data = [
        {
            "title": "Test Chat",
            "messages": [
                {"author": "user", "content": "Hello", "timestamp": "2024-05-12T10:00:00Z"},
                {"author": "assistant", "content": "Hi", "timestamp": "2024-05-12T10:00:01Z"}
            ]
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
    d = tmp_path / "claude.json"
    data = [
        {
            "name": "Claude Chat",
            "created_at": "2024-05-12T11:00:00Z",
            "chat_messages": [
                {"sender": "human", "text": "Help", "created_at": "2024-05-12T11:00:01Z"},
                {"sender": "assistant", "text": "Sure", "created_at": "2024-05-12T11:00:02Z"}
            ]
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
