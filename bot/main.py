import asyncio
from aiogram import Bot, Dispatcher
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from aiogram.types import BotCommand

from globals import (TG_TOKEN, ADMIN_TG_ID, TZ, POSTGRES_PASSWORD,
                     POSTGRES_USER, COMMANDS)
from apps import core, diary, notifications, admin
from apps.core.middleware import BlacklistMiddleware

bot = Bot(token=TG_TOKEN)

dp = Dispatcher()
dp.message.outer_middleware(BlacklistMiddleware())
dp.callback_query.outer_middleware(BlacklistMiddleware())

jobstores = {
    "default": SQLAlchemyJobStore(url=(
        f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}"
        "@postgres:5432/scheduler"
    ))
}

dp["scheduler"] = AsyncIOScheduler(timezone=TZ, jobstores=jobstores)

async def main():
    # Include the routers
    dp.include_routers(
        admin.router,
        notifications.router,
        diary.router,
        core.router,
    )

    dp["scheduler"].start()

    # Create the drop-up menu with the available commands
    await bot.set_my_commands([BotCommand(**cmd) for cmd in COMMANDS])

    # Notify the admin that the bot has started
    await bot.send_message(chat_id=ADMIN_TG_ID, text="START")

    try:
        await dp.start_polling(bot)
    except Exception as e:
        await bot.send_message(chat_id=ADMIN_TG_ID, text=e)

    # Notify the admin that the bot has stopped
    await bot.send_message(chat_id=ADMIN_TG_ID, text="STOP")

if __name__ == "__main__":
    asyncio.run(main())
