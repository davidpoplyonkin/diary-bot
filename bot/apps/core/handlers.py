from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.utils.formatting import Text, Bold, as_list

from .models import User
from globals import COMMANDS

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

    msg_lines = [
        Text(Bold("Ласкаво просимо до BioGraph (Біометричні графіки)!")),
        Text((
            "Радий бачити вас тут. Я допоможу вам стежити за важливими "
            "показниками вашого здоров’я та перетворювати сухі цифри на "
            "наочні звіти."
        )),
        Text("Введіть /help, щоб переглянути повний список доступних команд.")
    ]
    msg_text = as_list(*msg_lines)
    msg_kwargs = msg_text.as_kwargs()
    await message.answer(**msg_kwargs)

@router.message(Command("help"), StateFilter(None))
async def cmd_help(message: Message):
    """
    Prints the list of all available commands.
    """

    msg_lines = (
        [Text(Bold("Ось що я вмію:"))] +
        [Text(f"{cmd.get('command')} - {cmd.get('description')}") for cmd in COMMANDS]
    )
    msg_text = as_list(*msg_lines)
    msg_kwargs = msg_text.as_kwargs()
    await message.answer(**msg_kwargs)

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

    msg_text = Text(Bold("Скасувати"))
    msg_kwargs = msg_text.as_kwargs()
    await callback.message.answer(**msg_kwargs)

    await state.clear()

@router.message(StateFilter(None))
async def msg_unknown(message: Message):
    """
    If the user sends an unknown message, recommend them to type /help.
    """
    
    msg_lines = [
        Text(Bold("Команду не розпізнано.")),
        Text((
            "Перевірте правильність введення або скористайтеся "
            "розділом /help, де зібрані всі доступні функції та "
            "приклади записів."
        ))
    ]
    msg_text = as_list(*msg_lines)
    msg_kwargs = msg_text.as_kwargs()
    await message.answer(**msg_kwargs)
