from aiogram.utils.keyboard import InlineKeyboardBuilder

from globals import HEALTH_METRICS

def get_notifications_kb() -> InlineKeyboardBuilder:
    """
    Return a builder for a keyboard with scheduled notifications as
    buttons and also the add button at the end.
    """

    builder = InlineKeyboardBuilder()

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