import asyncio
import os
from pathlib import Path
from aiogram import Router, Bot, types
from aiogram.filters import Command

from .radio_core import queue, player

router = Router()

bot = Bot(os.getenv("BOT_TOKEN"))
OWNER_ID = int(os.getenv("OWNER_ID", "0"))

DB_INIT_LOCK = asyncio.Lock()


async def ensure_db() -> None:
    async with DB_INIT_LOCK:
        await queue.init_db()


@router.message(Command("join"))
async def join_cmd(message: types.Message) -> None:
    await ensure_db()
    play = player.get_player()
    await play.join(message.chat.id)
    await message.answer("Joined voice chat")


@router.message(Command("play"))
async def play_cmd(message: types.Message) -> None:
    await ensure_db()
    play = player.get_player()
    await play.play()
    await message.answer("Playback started")


@router.message(Command("stop"))
async def stop_cmd(message: types.Message) -> None:
    if message.from_user.id != OWNER_ID:
        await message.answer("🚫")
        return
    play = player.get_player()
    await play.stop()
    await message.answer("Stopped")


@router.message(Command("skip"))
async def skip_cmd(message: types.Message) -> None:
    if message.from_user.id != OWNER_ID:
        await message.answer("🚫")
        return
    play = player.get_player()
    await play.skip()
    await message.answer("Skipped")


@router.message(Command("queue"))
async def queue_cmd(message: types.Message) -> None:
    await ensure_db()
    tracks = await queue.get_confirmed()
    if not tracks:
        await message.answer("No tracks")
        return
    lines = [f"{tid}: {Path(path).name}" for tid, path in tracks]
    await message.answer("\n".join(lines))


@router.message(Command("suggest"))
async def suggest_cmd(message: types.Message) -> None:
    await ensure_db()
    if not message.audio or getattr(message.audio, "mime_type", "") != "audio/mpeg":
        await message.answer("Attach an mp3")
        return
    dest = queue.SUGGESTED_DIR / message.audio.file_name
    await bot.download(message.audio, destination=dest)
    await queue.add_track(message.from_user.id, dest, "pending", "user")
    await message.answer("Suggestion saved")


@router.message(Command("approve"))
async def approve_cmd(message: types.Message) -> None:
    if message.from_user.id != OWNER_ID:
        await message.answer("🚫")
        return
    parts = message.text.split()
    if len(parts) < 2:
        await message.answer("No id")
        return
    track_id = int(parts[1])
    info = await queue.get_track(track_id)
    if not info or info[2] != "pending":
        await message.answer("Not pending")
        return
    src = Path(info[1])
    dest = queue.CONFIRMED_DIR / src.name
    dest.write_bytes(src.read_bytes())
    await queue.update_status(track_id, "confirmed")
    await message.answer("Approved")


@router.message(Command("reject"))
async def reject_cmd(message: types.Message) -> None:
    if message.from_user.id != OWNER_ID:
        await message.answer("🚫")
        return
    parts = message.text.split()
    if len(parts) < 2:
        await message.answer("No id")
        return
    track_id = int(parts[1])
    info = await queue.get_track(track_id)
    if not info or info[2] != "pending":
        await message.answer("Not pending")
        return
    await queue.update_status(track_id, "rejected")
    await message.answer("Rejected")


@router.message()
async def private_upload(message: types.Message) -> None:
    if message.chat.type != "private":
        return
    if not message.audio:
        return
    if message.from_user.id != OWNER_ID:
        await message.answer("🚫")
        return
    await ensure_db()
    if getattr(message.audio, "mime_type", "") != "audio/mpeg":
        await message.answer("Attach an mp3")
        return
    dest = queue.CONFIRMED_DIR / message.audio.file_name
    await bot.download(message.audio, destination=dest)
    await queue.add_track(message.from_user.id, dest, "confirmed", "admin")
    await message.answer("Uploaded")
