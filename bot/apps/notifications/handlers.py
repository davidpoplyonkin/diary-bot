from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.filters import StateFilter

router = Router()

@router.message(Command("notifications"), StateFilter(None))
async def cmd_notifications(message: Message):
    """
    Answers to /notifications command with a list of scheduled
    notifications in chronological order.
    """

    await message.answer(
        "Scheduled notifications:",
        # reply_markup=??? # will be added sooner
    )