from aiogram.utils.keyboard import InlineKeyboardBuilder

def get_confirmation_kb(
        submit_callback_data: str
) -> InlineKeyboardBuilder:
    """
    Return a builder for a keyboard cancel and submit buttons.
    """

    builder = InlineKeyboardBuilder()

    builder.button(
        text="Скасувати",
        callback_data="cancel"
    )
    builder.button(
        text="Надіслати",
        callback_data=submit_callback_data
    )

    return builder

def get_cancel_btn() -> InlineKeyboardBuilder:
    """
    Return a builder for a cancel button.
    """

    builder = InlineKeyboardBuilder()
    builder.button(
        text="Скасувати",
        callback_data="cancel",
    )

    return builder