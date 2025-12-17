from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter
from aiogram.utils.formatting import Text, Bold
from aiogram.fsm.state import StatesGroup, State
from datetime import time
import re

from .markup import (get_notifications_kb, get_metrics_kb,
                     get_confirmation_kb, get_cancel_btn)
from .models import Notification
from globals import HEALTH_METRICS

router = Router()

class NotificationsSG(StatesGroup):
    time = State()

class ConfirmationSG(StatesGroup):
    confirmation = State()

@router.message(Command("notifications"), StateFilter(None))
async def cmd_notifications(message: Message):
    """
    Answers to /notifications command with a list of scheduled
    notifications in chronological order.
    """

    kb = await get_notifications_kb(
        user_tg_id=message.from_user.id
    )

    await message.answer(
        "Scheduled notifications:",
        reply_markup=kb.as_markup()
    )

@router.callback_query(F.data=="add-not", StateFilter(None))
async def btn_add_not(callback: CallbackQuery):
    """
    Ask the user for which metric they would like to receive
    notifications.
    """

    await callback.answer()

    # Remove the inline keyboard.
    msg_text = Text(Bold("Add"))
    msg_kwargs = msg_text.as_kwargs()
    msg_kwargs["reply_markup"] = None
    try:
        await callback.message.edit_text(**msg_kwargs)
    except:
        pass

    await callback.message.answer(
        text="Choose the metric you would like to receive notifications for:",
        reply_markup=get_metrics_kb().as_markup()
    )

@router.callback_query(F.data.startswith("add-not-"), StateFilter(None))
async def btn_add_not_hm(callback: CallbackQuery, state: FSMContext):
    """
    Ask the user when they would like to be notified.
    """

    await callback.answer()

    hm = callback.data.split("-")[2]
    hm_details = HEALTH_METRICS.get(hm)

    # Remove the inline keyboard.
    msg_text = Text(Bold(hm_details.get("button_text")))
    msg_kwargs = msg_text.as_kwargs()
    msg_kwargs["reply_markup"] = None
    try:
        await callback.message.edit_text(**msg_kwargs)
    except:
        pass

    n = await Notification.get_one(
        user_tg_id=callback.from_user.id,
        metric=hm
    )

    # Prevent the user from creating multiple notifications for the same metric.
    if n:
        await callback.message.answer("You already have a notification for this metric.")
        return

    await state.set_state(NotificationsSG.time)
    await state.update_data(hm=hm)

    await callback.message.answer(
        text="When would you like to be notified? (hh:mm)",
        reply_markup=get_cancel_btn().as_markup()
    )

@router.message(StateFilter(NotificationsSG.time))
async def msg_time(message: Message, state: FSMContext):
    """
    Save the notification to the database and also launch `aioschedule`.
    """

    str_time = message.text

    if re.fullmatch(r"^(\d{2}):(\d{2})$", str_time):
        h, m = map(int, str_time.split(":")) # Both are guaranteed to be
        # two-digit sequences

        if (h < 24) and (m < 60): # both are guaranteed to be
            # non-negative

            state_data = await state.get_data()
            await state.clear()

            # Save to the database.
            await Notification.insert_one(
                user_tg_id=message.from_user.id,
                metric=state_data.get("hm"),
                time=time(h, m),
            )

            msg_text = Text(Bold("Done"))
            msg_kwargs = msg_text.as_kwargs()
            await message.answer(**msg_kwargs)

            return

    await message.answer("Invalid input. Expected format is 'hh:mm'. Try again:")

@router.callback_query(F.data.startswith("del-not-"), StateFilter(None))
async def btn_del_not(callback: CallbackQuery, state: FSMContext):
    """
    Ask whether they are sure they want to delete the specified notification.
    """

    await callback.answer()

    hm = callback.data.split("-")[2]
    hm_details = HEALTH_METRICS.get(hm)

    # Remove the inline keyboard.
    msg_text = Text(Bold("Delete"), " ", hm_details.get("button_text"))
    msg_kwargs = msg_text.as_kwargs()
    msg_kwargs["reply_markup"] = None
    try:
        await callback.message.edit_text(**msg_kwargs)
    except:
        pass

    await state.set_state(ConfirmationSG.confirmation)
    await state.update_data(hm=hm)

    await callback.message.answer(
        text=(
            "Are you sure you want to delete the "
            f"{hm_details.get('button_text')} notification"
        ),
        reply_markup=get_confirmation_kb().as_markup()
    )

@router.callback_query(F.data=="cancel-del-not", StateFilter(ConfirmationSG.confirmation))
@router.callback_query(F.data=="cancel-not", StateFilter(NotificationsSG.time))
async def btn_cancel(callback: CallbackQuery, state: FSMContext):
    """
    Clear the state.
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

@router.callback_query(F.data=="submit-del-not", StateFilter(ConfirmationSG.confirmation))
async def btn_submit(callback: CallbackQuery, state: FSMContext):
    """
    Submit the sequence of health metrics.
    """

    await callback.answer()

    try:
        await callback.message.edit_reply_markup(reply_markup=None)
    except:
        pass

    state_data = await state.get_data()
    hm = state_data.get("hm")

    # Get the user Telegram ID
    user_tg_id = callback.from_user.id

    # Delete the notification from the database
    await Notification.delete_many(user_tg_id, hm)

    # Let the user know that this metric was deleted
    await callback.message.answer("Done")

    await state.clear()