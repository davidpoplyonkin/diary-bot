from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery

from .models import User

class BlacklistMiddleware(BaseMiddleware):
    """
    Prevent blacklisted users from using the bot.
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

        user = await User.get_one(user_tg_id)
        if (user):
            if (user.get("is_blacklisted")):
                # Notify the user they were blacklisted.
                return await message.answer("You were blacklisted.")
            
            # Run the handler.
            return await handler(event, data)
        else:
            if message.text == "/start":
                # Run the handler.
                return await handler(event, data)
        
            # Recommend the user to run the /start command. This should add
            # their record to the database.
            return await message.answer((
                "Something went wrong. Run the /start command and try "
                "again."
            ))
