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
