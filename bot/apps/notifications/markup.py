from aiogram.utils.keyboard import InlineKeyboardBuilder
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from globals import HEALTH_METRICS

async def get_notifications_kb(
        user_tg_id: int,
        scheduler: AsyncIOScheduler
    ) -> InlineKeyboardBuilder:
    """
    Return a builder for a keyboard with scheduled notifications as
    buttons and also the add button at the end.
    """

    builder = InlineKeyboardBuilder()

    jobs = scheduler.get_jobs()
    jobs.sort(key=lambda job: job.kwargs.get("time"))

    for job in jobs:
        if job.id.startswith(str(user_tg_id)):
            hm = job.kwargs.get("metric")
            hm_details = HEALTH_METRICS.get(hm)

            builder.button(
                text=f"🗑️ {job.kwargs.get('time')} {hm_details.get('button_text')}",
                callback_data=f"del-not-{hm}"
            )

    builder.button(
        text="+",
        callback_data="add-not"
    )

    builder.adjust(1)

    return builder

def get_metrics_kb() -> InlineKeyboardBuilder:
    """
    Return a builder for a keyboard with scheduled notifications as
    buttons and also the add button at the end.
    """

    builder = InlineKeyboardBuilder()

    for hm, details in HEALTH_METRICS.items():
        if (details.get("first")):
            builder.button(
                text=details.get("button_text"),
                callback_data=f"add-not-{hm}"
            )

    builder.adjust(1)

    return builder
