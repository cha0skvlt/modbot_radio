"""Voice player built on Telethon + PyTgCalls."""

from __future__ import annotations

import asyncio
import os
from pathlib import Path

import ffmpeg
from telethon import TelegramClient
from telethon.sessions import StringSession
from pytgcalls import PyTgCalls

from . import queue


API_ID = int(os.getenv("API_ID", "0"))
API_HASH = os.getenv("API_HASH", "")
SESSION = os.getenv("USERBOT_SESSION", "")


class Player:
    def __init__(self) -> None:
        self.client = TelegramClient(StringSession(SESSION), API_ID, API_HASH)
        self.calls = PyTgCalls(self.client)
        self.chat_id: int | None = None
        self._task: asyncio.Task | None = None
        self._skip = asyncio.Event()
        self._stop = asyncio.Event()

    async def join(self, chat_id: int) -> None:
        self.chat_id = chat_id
        if not self.client.is_connected():
            await self.client.start()
            await self.calls.start()

    async def play(self) -> None:
        if self.chat_id is None:
            raise RuntimeError("join first")
        if self._task and not self._task.done():
            return
        self._stop.clear()
        self._task = asyncio.create_task(self._loop())

    async def stop(self) -> None:
        self._stop.set()
        if self._task:
            await self._task
        if self.chat_id is not None:
            await self.calls.leave_group_call(self.chat_id)
        self.chat_id = None

    async def skip(self) -> None:
        self._skip.set()

    async def _loop(self) -> None:
        assert self.chat_id is not None
        index = 0
        while not self._stop.is_set():
            tracks = await queue.get_confirmed()
            if not tracks:
                await asyncio.sleep(3)
                continue
            track = Path(tracks[index % len(tracks)][1])
            process = (
                ffmpeg.input(str(track))
                .output(
                    "pipe:",
                    format="s16le",
                    acodec="pcm_s16le",
                    ac=2,
                    ar="48000",
                )
                .run_async(pipe_stdout=True)
            )
            await self.calls.join_group_call(self.chat_id, process.stdout)
            while process.poll() is None:
                if self._skip.is_set() or self._stop.is_set():
                    process.terminate()
                    self._skip.clear()
                    break
                await asyncio.sleep(1)
            await self.calls.leave_group_call(self.chat_id)
            index += 1
        self._skip.clear()


def get_player() -> Player:
    global _player
    try:
        return _player
    except NameError:
        _player = Player()
        return _player
