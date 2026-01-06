from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery
from aiogram.utils.formatting import Bold, Text, as_list

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
                
                msg_lines = [
                    Text("🚫 ", Bold("Вас додано до чорного списку")),
                    Text((
                        "Ми зафіксували надто велику кількість запитів, що "
                        "схоже на автоматичний спам. Для збереження "
                        "стабільності системи ваш доступ було припинено."
                    )),
                    Text((
                        "Нам прикро, що так сталося, але ми дбаємо про "
                        "безпеку усіх наших пацієнтів."
                    ))
                ]
                msg_text = as_list(*msg_lines)
                msg_kwargs = msg_text.as_kwargs()

                # Notify the user they were blacklisted.
                return await message.answer(**msg_kwargs)
            
            # Run the handler.
            return await handler(event, data)
        else:
            if message.text == "/start":
                # Run the handler.
                return await handler(event, data)

            msg_text = Text("Щось пішло не так. Введіть /start і спробуйте ще раз.")
            msg_kwargs = msg_text.as_kwargs()

            # Recommend the user to run the /start command. This should add
            # their record to the database.
            return await message.answer(**msg_kwargs)
