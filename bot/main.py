import asyncio
from aiogram import Bot, Dispatcher
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore

from globals import (TG_TOKEN, ADMIN_TG_ID, IANA_TZ, POSTGRES_PASSWORD,
                     POSTGRES_USER)
from apps import core, diary, notifications

bot = Bot(token=TG_TOKEN)
dp = Dispatcher()

jobstores = {
    "default": SQLAlchemyJobStore(url=(
        f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}"
        "@postgres:5432/scheduler"
    ))
}

dp["scheduler"] = AsyncIOScheduler(timezone=IANA_TZ, jobstores=jobstores)

async def main():
    # Create tables
    await core.User.create_table()
    await diary.HealthMetric.create_table()

    # Include the routers
    dp.include_routers(
        notifications.router,
        diary.router,
        core.router,
    )

    dp["scheduler"].start()

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