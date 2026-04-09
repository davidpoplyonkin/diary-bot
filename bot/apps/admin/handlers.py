from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from .middleware import AdminOnlyMiddleware
from ..core.markup import get_confirmation_kb
from ..core.handlers import ConfirmationSG
from ..api import UserClient

router = Router()
router.message.middleware(AdminOnlyMiddleware())
router.callback_query.middleware(AdminOnlyMiddleware())

class ChartSG(StatesGroup):
    window = State()

@router.callback_query(F.data.startswith("blacklist-"), StateFilter(None))
async def btn_blacklist(callback: CallbackQuery, state: FSMContext):
    """
    Ask the admin to confirm they want to blacklist the user.
    """

    await callback.answer("")

    user_tg_id = callback.data.split("-")[1]

    await state.set_state(ConfirmationSG.confirmation)
    await state.update_data(user_tg_id=user_tg_id)

    await callback.message.answer(
        text="Are you sure you want to blacklist this user?",
        reply_markup=get_confirmation_kb("submit-blacklist").as_markup()
    )

@router.callback_query(F.data=="submit-blacklist", StateFilter(ConfirmationSG.confirmation))
async def btn_submit(callback: CallbackQuery, state: FSMContext):
    """
    Blacklist the specified user.
    """

    await callback.answer("")

    # Remove the inline keyboard
    try:
        await callback.message.edit_reply_markup(reply_markup=None)
    except:
        pass

    state_data = await state.get_data()
    await state.clear()
    user_tg_id = int(state_data.get("user_tg_id"))

    async with UserClient() as client:
        user = await client.blacklist_user(user_tg_id)

    if user is None:
        await callback.message.answer("User not found")
    else:
        await callback.message.answer("Done")
