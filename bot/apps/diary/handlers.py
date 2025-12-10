from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.filters import StateFilter

from .markup import get_health_metrics_kb

router = Router()

@router.message(Command("enter"), StateFilter(None))
async def cmd_enter(message: Message):
    """
    Answers to /enter with a list of available health metrics.
    """

    await message.answer(
        "Choose one of the following health metrics:",
        reply_markup=get_health_metrics_kb().as_markup()
    )