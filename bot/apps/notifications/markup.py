from aiogram.utils.keyboard import InlineKeyboardBuilder

from globals import HEALTH_METRICS
from .models import Notification

async def get_notifications_kb(user_tg_id) -> InlineKeyboardBuilder:
    """
    Return a builder for a keyboard with scheduled notifications as
    buttons and also the add button at the end.
    """

    builder = InlineKeyboardBuilder()

    notifications = await Notification.get_many(user_tg_id)

    for n in notifications:
        hm = n.get("metric")
        hm_details = HEALTH_METRICS.get(hm)

        builder.button(
            text=f"🗑️ {n.get('time')} {hm_details.get('button_text')}",
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

def get_confirmation_kb() -> InlineKeyboardBuilder:
    """
    Return a builder for a keyboard cancel and submit buttons.
    """

    builder = InlineKeyboardBuilder()

    builder.button(
        text="Cancel",
        callback_data="cancel-del-not"
    )
    builder.button(
        text="Submit",
        callback_data="submit-del-not"
    )

    builder.adjust(2)

    return builder

def get_cancel_btn() -> InlineKeyboardBuilder:
    """
    Return a builder for a cancel button.
    """

    builder = InlineKeyboardBuilder()
    builder.button(
        text="Cancel",
        callback_data="cancel-not",
    )

    return builder
