from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery

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
        
        return await message.answer("This is an admin-only command.")
