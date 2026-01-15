from aiogram.utils.keyboard import InlineKeyboardBuilder

from globals import HEALTH_METRICS

def get_health_metrics_kb() -> InlineKeyboardBuilder:
    """
    Return a builder for a keyboard with health metrics names as
    buttons.
    """

    builder = InlineKeyboardBuilder()

    for hm, details in HEALTH_METRICS.items():
        if details.get("first"):
            builder.button(
                text=details["button_text"],
                callback_data=f"enter-{hm}"
            )

    builder.adjust(1)

    return builder


def get_summary_kb(user_tg_id, metric) -> InlineKeyboardBuilder:
    """
    Return a builder for a keyboard to attach to the message sent to
    the admin.
    """

    builder = InlineKeyboardBuilder()

    builder.button(
        text="Chart",
        callback_data=f"chart-{user_tg_id}-{metric}"
    )

    builder.button(
        text="Blacklist",
        callback_data=f"blacklist-{user_tg_id}"
    )

    builder.adjust(1)

    return builder