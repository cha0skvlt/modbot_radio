import asyncio
import importlib
import os
from pathlib import Path

import aiosqlite
import pytest


class FakeAudio:
    def __init__(self, name: str = "track.mp3") -> None:
        self.file_name = name


class FakeUser:
    def __init__(self, user_id: int):
        self.id = user_id


class FakeChat:
    def __init__(self, chat_type: str = "private"):
        self.type = chat_type
        self.id = 1


class FakeMessage:
    def __init__(self, user_id: int, text: str = "", audio: FakeAudio | None = None):
        self.from_user = FakeUser(user_id)
        self.chat = FakeChat()
        self.text = text
        self.audio = audio
        self.answers: list[str] = []

    async def answer(self, text: str) -> None:
        self.answers.append(text)


@pytest.mark.asyncio
async def test_suggest_and_approve(tmp_path, monkeypatch):
    monkeypatch.setenv("BOT_TOKEN", "12345:TEST")
    monkeypatch.setenv("OWNER_ID", "5")
    monkeypatch.setenv("RADIO_DB", str(tmp_path / "db.sqlite"))
    monkeypatch.setenv("UPLOADS_DIR", str(tmp_path / "upl"))
    radio = importlib.reload(importlib.import_module("modules.radio"))

    msg = FakeMessage(7, text="/suggest", audio=FakeAudio())
    await radio.suggest_cmd(msg)
    assert any("saved" in a.lower() for a in msg.answers)

    async with aiosqlite.connect(radio.queue.DB_PATH) as db:
        async with db.execute("SELECT id FROM tracks WHERE status='pending'") as cur:
            row = await cur.fetchone()
            pending_id = row[0]

    approve_msg = FakeMessage(5, text=f"/approve {pending_id}")
    await radio.approve_cmd(approve_msg)
    async with aiosqlite.connect(radio.queue.DB_PATH) as db:
        async with db.execute(
            "SELECT status FROM tracks WHERE id=?", (pending_id,)
        ) as cur:
            row = await cur.fetchone()
            assert row[0] == "confirmed"
