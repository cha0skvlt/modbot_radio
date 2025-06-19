import os
from datetime import datetime
from pathlib import Path
import aiosqlite

DB_PATH = os.getenv("RADIO_DB", "radio.db")
BASE_UPLOADS = Path(os.getenv("UPLOADS_DIR", "uploads"))
CONFIRMED_DIR = BASE_UPLOADS / "confirmed"
SUGGESTED_DIR = BASE_UPLOADS / "suggested"


async def init_db() -> None:
    os.makedirs(CONFIRMED_DIR, exist_ok=True)
    os.makedirs(SUGGESTED_DIR, exist_ok=True)
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            """
            CREATE TABLE IF NOT EXISTS tracks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                path TEXT NOT NULL,
                status TEXT NOT NULL,
                added_by TEXT NOT NULL,
                timestamp TEXT NOT NULL
            )
            """
        )
        await db.commit()


async def add_track(user_id: int, path: Path, status: str, added_by: str) -> int:
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "INSERT INTO tracks (user_id, path, status, added_by, timestamp) VALUES (?, ?, ?, ?, ?)",
            (user_id, str(path), status, added_by, datetime.utcnow().isoformat()),
        )
        await db.commit()
        cur = await db.execute("SELECT last_insert_rowid()")
        row = await cur.fetchone()
        return row[0]


async def update_status(track_id: int, status: str) -> None:
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "UPDATE tracks SET status=? WHERE id=?",
            (status, track_id),
        )
        await db.commit()


async def get_confirmed() -> list[tuple[int, str]]:
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute(
            "SELECT id, path FROM tracks WHERE status='confirmed' ORDER BY id"
        ) as cur:
            return await cur.fetchall()


async def get_track(track_id: int):
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute(
            "SELECT id, path, status FROM tracks WHERE id=?", (track_id,)
        ) as cur:
            return await cur.fetchone()
