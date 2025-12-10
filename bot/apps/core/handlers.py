from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.filters import StateFilter

router = Router()

@router.message(CommandStart(), StateFilter(None))
async def cmd_start(message: Message):
    """
    Answers to /start.
    """

    await message.answer("Hello World!")