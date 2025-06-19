# Test suite for the /start command

import asyncio
import importlib
import os
import sys

import pytest

sys.path.insert(0, os.getcwd())


class FakeUser:
    def __init__(self, user_id: int):
        self.id = user_id


class FakeMessage:
    def __init__(self, user_id: int):
        self.from_user = FakeUser(user_id)
        self.answers = []

    async def answer(self, text: str) -> None:
        self.answers.append(text)


def test_start_allowed(monkeypatch):
    monkeypatch.setenv("BOT_TOKEN", "123456:TESTTOKEN")
    monkeypatch.setenv("OWNER_ID", "5")
    bot_module = importlib.reload(importlib.import_module("bot"))
    msg = FakeMessage(5)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(bot_module.start_cmd(msg))
    assert any("Status: OK" in t for t in msg.answers)


def test_start_denied(monkeypatch):
    monkeypatch.setenv("BOT_TOKEN", "123456:TESTTOKEN")
    monkeypatch.setenv("OWNER_ID", "5")
    bot_module = importlib.reload(importlib.import_module("bot"))
    msg = FakeMessage(7)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(bot_module.start_cmd(msg))
    assert msg.answers == ["🚫 Access denied."]
