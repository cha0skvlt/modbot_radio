# 🤖 MODBOT — Modular Telegram Bot Framework v.1.0

A minimalistic, production-ready Telegram bot skeleton using **aiogram 3**.

---

## 🔒 License

This is a **closed, proprietary project**.  
All rights reserved. Unauthorized use is strictly prohibited.  
See [LICENSE](./LICENSE) for details.

---
## 📌 Goal

Create a modular bot architecture:

- `bot.py` — single entrypoint, loads everything
- `modules/` — feature plugins (auto-loaded)
- `.env` — all config in one file (no hardcoded secrets)
- `/start` — the only built-in command, with uptime and loaded modules

---

## 🧠 Features

- 🧩 Modular design — logic lives in `modules/`, not in `bot.py`
- 🔁 Auto-loads all `*.py` files from `modules/`
- 🔐 Owner-only access — `/start` replies only to the OWNER_ID
- ✅ Built-in tests
- 🧪 GitHub Actions CI: `pytest` + `black`

---

## 🛠 Technologies

![Chaos-Tested](https://img.shields.io/badge/Chaos--Tested-red?style=flat-square)
![Python](https://img.shields.io/badge/Python-3.12-blue?logo=python)
![Aiogram](https://img.shields.io/badge/aiogram-3.4.x-lightgrey)
![black](https://img.shields.io/badge/code%20style-black-black?style=flat-square)
![pytest](https://img.shields.io/badge/tests-pytest-green?style=flat-square)
![CI](https://img.shields.io/github/actions/workflow/status/cha0skvlt/modbot/ci.yml?label=CI&style=flat-square)

---

## 🚀 Usage

### 1. Clone & configure

```bash
git clone https://github.com/cha0skvlt/modbot
cd modbot
cp .env.example .env
```

Edit `.env`:

```dotenv
BOT_TOKEN=123456:ABCDEF...
OWNER_ID=123456789
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Run

```bash
python bot.py
```

---

## ✅ Included commands

- `/start` → status + uptime (owner-only)

---

## 🧪 Tests

Run tests with:

```bash
pytest
```

---

## 🔄 Module structure

Any file inside `modules/` with a `router` object is auto-loaded:

```python
# modules/hello.py
from aiogram import Router
router = Router()

@router.message()
async def hi(msg): await msg.answer("Hi!")
```

---

## 🧱 Example `.env`

```dotenv
BOT_TOKEN=123456789:ABCDEF...
OWNER_ID=123456789
```

---

## 🧼 Linting

We enforce `black` code style.

Run formatter:

```bash
black .
```

---

## 📦 Coming Soon

- Dockerfile + Compose
- Healthcheck endpoint
- Live module reload

---

Made  by [cha0skvlt]

