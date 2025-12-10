from aiogram import Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from aiogram.filters import StateFilter

router = Router()

@router.message(CommandStart(), StateFilter(None))
async def cmd_start(message: Message):
    """
    Answers to /start.
    """

    await message.answer("Hello World!")

@router.message(Command("help"), StateFilter(None))
async def cmd_help(message: Message):
    """
    Prints the list of all available commands.
    """

    await message.answer((
        "/start - Start the first conversation with the bot\n"
        "/help - Print the list of all available commands"
    ))
