import importlib
import os
import sys


def test_bot_env(monkeypatch):
    monkeypatch.setenv("BOT_TOKEN", "123456:TESTTOKEN")
    sys.path.insert(0, os.getcwd())
    bot_module = importlib.reload(importlib.import_module("bot"))
    assert bot_module.bot.token == "123456:TESTTOKEN"
