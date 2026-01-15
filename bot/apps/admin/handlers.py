from aiogram import Router, F, Bot
from aiogram.types import CallbackQuery, Message
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.utils.formatting import Text
from datetime import datetime
from zoneinfo import ZoneInfo

from .middleware import AdminOnlyMiddleware
from ..core.markup import get_confirmation_kb, get_cancel_btn
from ..core.handlers import ConfirmationSG
from ..core.models import User
from charts import reply_chart
from globals import TZ

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

    await User.blacklist(user_tg_id)

    await callback.message.answer("Done")

@router.callback_query(F.data.startswith("chart-"), StateFilter(None))
async def btn_chart(callback: CallbackQuery, state: FSMContext):
    """
    Ask the admin how many days of data to use to build the chart.
    """

    await callback.answer("")

    _, user_tg_id, metric = callback.data.split("-")

    # Set the state of waiting for the number of days
    await state.set_state(ChartSG.window)

    await state.update_data(
        user_tg_id=user_tg_id,
        metric=metric
    )

    msg_text = Text("Enter how many days of data to use:")
    msg_kwargs = msg_text.as_kwargs()
    msg_kwargs["reply_markup"] = get_cancel_btn().as_markup()

    # Send the message to the admin
    ans = await callback.message.answer(**msg_kwargs)

    # Record the answer ID in order to then remove the attached cancel
    # button
    await state.update_data(
        ans_msg_id=ans.message_id,
        ans_chat_id=ans.chat.id,
    )

@router.message(StateFilter(ChartSG.window))
async def msg_window(message: Message, state: FSMContext, bot: Bot):
    """
    Ask the admin how many days of data to use to build the chart.
    """

    state_data = await state.get_data()

    # Remove the cancel button.
    try:
        await bot.edit_message_reply_markup(
            chat_id=state_data.get("ans_chat_id"),
            message_id=state_data.get("ans_msg_id"),
            reply_markup=None
        )
    except:
        pass

    # Validate user input.
    input_valid = False
    try:
        val = int(message.text)
        if (val > 0):
            input_valid = True
    except:
        pass

    if not input_valid:
        # Don't change the state and ask the user to enter a valid
        # number.
        msg_text = Text("Invalid input. Enter a positive number:")
        msg_kwargs = msg_text.as_kwargs()
        msg_kwargs["reply_markup"] = get_cancel_btn().as_markup()

        ans = await message.answer(**msg_kwargs)

        # Record the answer ID in order to then remove the attached cancel
        # button
        await state.update_data(
            ans_msg_id=ans.message_id,
            ans_chat_id=ans.chat.id,
        )

        return
    
    await state.clear()

    # Get today's date in the bot's timezone
    date_utc = datetime.now(ZoneInfo("UTC"))
    date_tz = date_utc.astimezone(ZoneInfo(TZ))

    await reply_chart(
        message=message,
        user_tg_id=int(state_data.get("user_tg_id")),
        metric=state_data.get("metric"),
        date=date_tz,
        window=val
    )
