from aiogram import Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from aiogram.filters import StateFilter

from .models import User

router = Router()

@router.message(CommandStart(), StateFilter(None))
async def cmd_start(message: Message):
    """
    Answers to /start.
    """

    await User.upsert_one(
        tg_id=message.from_user.id,
        full_name=message.from_user.full_name,
    )

    await message.answer("Hello World!")

@router.message(Command("help"), StateFilter(None))
async def cmd_help(message: Message):
    """
    Prints the list of all available commands.
    """

    await message.answer((
        "/start - Start the first conversation with the bot\n"
        "/help - Print the list of all available commands\n"
        "/enter - Print the list of all available health metrics\n"
        "/notifications - Print the list of all scheduled notifications"
    ))

@router.message(StateFilter(None))
async def default_handler(message: Message):
    """
    If the user sends an unknown message, recommend them to type /help.
    """

    await message.answer("Type /help, to get the list of all available commands.")
