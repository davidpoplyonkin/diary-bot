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

def get_cancel_btn() -> InlineKeyboardBuilder:
    """
    Return a builder for a cancel button.
    """

    builder = InlineKeyboardBuilder()
    builder.button(
        text="Cancel",
        callback_data="cancel-hm",
    )

    return builder

def get_confirmation_kb() -> InlineKeyboardBuilder:
    """
    Return a builder for a keyboard cancel and submit buttons.
    """

    builder = InlineKeyboardBuilder()

    builder.button(
        text="Cancel",
        callback_data=f"cancel-hm"
    )
    builder.button(
        text="Submit",
        callback_data=f"submit-hm"
    )

    builder.adjust(2)

    return builder
