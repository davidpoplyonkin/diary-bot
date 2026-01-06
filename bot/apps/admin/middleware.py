from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery
from aiogram.utils.formatting import Text

from globals import ADMIN_TG_ID

class AdminOnlyMiddleware(BaseMiddleware):
    """
    Prevent the non-admin users from running certain commands.
    """

    async def __call__(self, handler, event, data):
        
        if isinstance(event, Message):
            user_tg_id = event.from_user.id
            message = event
        elif isinstance(event, CallbackQuery):
            await event.answer("")
            user_tg_id = event.from_user.id
            message = event.message
        else:
            # Ignore everything, else.
            return

        if (user_tg_id == int(ADMIN_TG_ID)):
            return await handler(event, data)
        
        msg_text = Text("Це команда лише для адміністратора.")
        msg_kwargs = msg_text.as_kwargs()
        return await message.answer(**msg_kwargs)
