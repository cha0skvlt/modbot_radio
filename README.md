# 🎧 modbot.modules.radio

## 📌 Purpose

Radio module for `modbot`. Plays 24/7 music in Telegram voice chat via userbot.  
Only OWNER and admins can upload tracks. Others can suggest via `/suggest`.

---

## 🔧 Features

- Stream audio from `uploads/confirmed/*` using PyTgCalls
- Accept private uploads from OWNER/admins
- Non-admin users can suggest tracks (pending review)
- Commands:
  - `/join` — join voice chat
  - `/play` — start playing loop
  - `/skip` — skip current track (admin only)
  - `/stop` — stop playback
  - `/queue` — show upcoming tracks
  - `/suggest` — suggest track to admins
  - `/approve <id>` / `/reject <id>` — review suggestions

---

## 📂 Structure

```text
modules/
├── radio.py            # Command interface
├── radio_core/
│   ├── player.py       # Stream control (loop, skip, ffmpeg)
│   └── queue.py        # Track queue from SQLite
uploads/
├── confirmed/          # Tracks accepted to stream
└── suggested/          # Pending tracks (user suggestions)
```

---

## 🗃️ Database schema (aiosqlite)

`tracks` table:

| Column     | Type     | Description                    |
|------------|----------|--------------------------------|
| id         | INTEGER  | Autoincrement                  |
| user_id    | INTEGER  | Telegram ID                    |
| path       | TEXT     | File path                      |
| status     | TEXT     | 'confirmed' / 'pending' / 'rejected' |
| added_by   | TEXT     | 'admin' / 'user'               |
| timestamp  | TEXT     | ISO datetime                   |

---

## 🚀 Requirements

- `telethon` — userbot client
- `pytgcalls` — stream engine
- `ffmpeg-python` — audio processing
- `aiosqlite` — track storage
- `aiogram` — bot interface

All listed in `requirements.txt`

---

## 🧠 Notes

- Stream runs via `userbot`, requires valid session file
- Tracks must be short and safe (max duration, size limits)
- Only confirmed tracks are looped in stream
- Suggestions require manual approval

---

## ✅ Status

> MVP stage. Supports full radio cycle + suggestion flow.


