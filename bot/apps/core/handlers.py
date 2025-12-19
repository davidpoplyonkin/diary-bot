from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.utils.formatting import Text, Bold

from .models import User

router = Router()

class ConfirmationSG(StatesGroup):
    confirmation = State()

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

@router.callback_query(F.data=="cancel")
async def btn_cancel(callback: CallbackQuery, state: FSMContext):
    """
    Clear the state
    """

    await callback.answer()

    # Remove the inline keyboard.
    try:
        await callback.message.edit_reply_markup(reply_markup=None)
    except:
        pass

    msg_text = Text(Bold("Cancel"))
    msg_kwargs = msg_text.as_kwargs()
    await callback.message.answer(**msg_kwargs)

    await state.clear()

@router.message(StateFilter(None))
async def msg_unknown(message: Message):
    """
    If the user sends an unknown message, recommend them to type /help.
    """

    await message.answer("Type /help, to get the list of all available commands.")
