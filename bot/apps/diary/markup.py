from aiogram.utils.keyboard import InlineKeyboardBuilder

from globals import HEALTH_METRICS

def get_health_metrics_kb() -> InlineKeyboardBuilder:
    """
    Return a builder for a keyboard with health metrics names as
    buttons.
    """

    builder = InlineKeyboardBuilder()

    for i, hm in enumerate(HEALTH_METRICS):
        builder.button(
            text=hm["verbose"],
            callback_data=f"enter-hm_{i}"
        )

    builder.adjust(1)

    return builder