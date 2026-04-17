from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types.web_app_info import WebAppInfo

from globals import HEALTH_METRICS, DASHBOARD_URL

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

    # Open the dashboard mini-app
    builder.button(
        text="Chart",
        web_app=WebAppInfo(url=(
            f"{DASHBOARD_URL}"
            f"/?patient={user_tg_id}"
            f"&metric={metric}"
        ))
    )

    builder.button(
        text="Blacklist",
        callback_data=f"blacklist-{user_tg_id}"
    )

    builder.adjust(1)

    return builder