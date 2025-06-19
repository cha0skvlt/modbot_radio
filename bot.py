import os
import asyncio
import importlib
import pkgutil
from datetime import datetime
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

load_dotenv()  # pull secrets from .env

TOKEN = os.getenv("BOT_TOKEN")  # your bot token
OWNER_ID = int(os.getenv("OWNER_ID", "0"))

if not TOKEN:
    raise RuntimeError("BOT_TOKEN not set")

if not OWNER_ID:
    raise RuntimeError("OWNER_ID not set")

bot = Bot(TOKEN)
dp = Dispatcher()  # central dispatcher
START_TIME = datetime.now()


@dp.message(Command("start"))
async def start_cmd(message: types.Message) -> None:
    if message.from_user.id != OWNER_ID:
        await message.answer("🚫 Access denied.")
        return
    delta = datetime.now() - START_TIME
    days = delta.days
    hours = delta.seconds // 3600
    modules = [
        n for _, n, _ in pkgutil.iter_modules(["modules"]) if not n.startswith("_")
    ]
    mods = ", ".join(modules) if modules else "none"
    await message.answer(
        f"Status: OK\nup for {days}d {hours}h\nLoaded modules: {mods}\nbot core by @cha0skvlt"
    )


async def on_startup():
    """Load routers from modules package."""
    for finder, name, ispkg in pkgutil.iter_modules(["modules"]):
        if name.startswith("_"):
            continue
        try:
            module = importlib.import_module(f"modules.{name}")
            router = getattr(module, "router")
        except (ImportError, AttributeError) as e:
            print(f"Failed to load module {name}: {e}")
            continue
        if router:
            dp.include_router(router)


async def main():
    """Entry point for running bot."""
    await on_startup()
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
