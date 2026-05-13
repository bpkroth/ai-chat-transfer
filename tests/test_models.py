from datetime import datetime

from chat_bridge.models import ChatHistory, ExportData, Message


def test_message_creation():
    msg = Message(role="user", content="Hello")
    assert msg.role == "user"
    assert msg.content == "Hello"
    assert msg.timestamp is None
    assert msg.metadata == {}


def test_chat_history_creation():
    msg = Message(role="assistant", content="Hi there")
    chat = ChatHistory(messages=[msg], source="test", created_at=datetime.now())
    assert len(chat.messages) == 1
    assert chat.source == "test"
    assert chat.messages[0].content == "Hi there"


def test_export_data_serialization():
    msg = Message(role="user", content="Test")
    chat = ChatHistory(messages=[msg], source="test", created_at=datetime.now())
    export = ExportData(chats=[chat])

    json_data = export.model_dump_json()
    assert "test" in json_data
    assert "Test" in json_data
