from aiogram import Router, F, Bot
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter
from aiogram.utils.formatting import Text, Bold, as_list
from aiogram.fsm.state import StatesGroup, State
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import re

from .markup import get_notifications_kb, get_metrics_kb
from ..core.markup import get_confirmation_kb, get_cancel_btn
from ..core.handlers import ConfirmationSG
from globals import HEALTH_METRICS
from .helpers import notify

router = Router()

class NotificationsSG(StatesGroup):
    time = State()

@router.message(Command("notifications"), StateFilter(None))
async def cmd_notifications(message: Message, scheduler: AsyncIOScheduler):
    """
    Answers to /notifications command with a list of scheduled
    notifications in chronological order.
    """

    kb = await get_notifications_kb(
        user_tg_id=message.from_user.id,
        scheduler=scheduler
    )

    await message.answer(
        "Заплановані сповіщення",
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
        text="Оберіть для якого параметру слід зробити нагадування:",
        reply_markup=get_metrics_kb().as_markup()
    )

@router.callback_query(F.data.startswith("add-not-"), StateFilter(None))
async def btn_add_not_hm(
    callback: CallbackQuery,
    state: FSMContext,
    scheduler: AsyncIOScheduler
):
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

    # Prevent the user from creating multiple notifications for the same metric.
    if scheduler.get_job(f"{callback.from_user.id}-{hm}"):
        await callback.message.answer("У вас уже є сповіщення для цього показника.")
        return

    await state.set_state(NotificationsSG.time)
    await state.update_data(hm=hm)

    ans = await callback.message.answer(
        text="Тепер напишіть мені час у форматі «гг:хх»:",
        reply_markup=get_cancel_btn().as_markup()
    )

    # Record the answer ID in order to then remove the attached cancel
    # button
    await state.update_data(
        ans_msg_id=ans.message_id,
        ans_chat_id=ans.chat.id,
    )

@router.message(StateFilter(NotificationsSG.time))
async def msg_time(
    message: Message,
    state: FSMContext,
    bot: Bot,
    scheduler: AsyncIOScheduler
):
    """
    Schedule the notification.
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

    str_time = message.text

    if re.fullmatch(r"^(\d{2}):(\d{2})$", str_time):
        h, m = map(int, str_time.split(":")) # Both are guaranteed to be
        # two-digit sequences

        if (h < 24) and (m < 60): # both are guaranteed to be
            # non-negative

            await state.clear()

            hm = state_data.get("hm")
            user_tg_id = message.from_user.id

            scheduler.add_job(
                id=f"{user_tg_id}-{hm}",
                replace_existing=True,
                func=notify,
                kwargs={
                    "user_tg_id": user_tg_id,
                    "metric": hm,
                    "time": str_time,
                },
                trigger="cron",
                hour=h,
                minute=m,
            )

            msg_text = Text("👌 ", Bold("Готово! "), "Ви завжди можете видалити це сповіщення в меню /notifications.")
            msg_kwargs = msg_text.as_kwargs()
            await message.answer(**msg_kwargs)

            return

    await message.answer("Очікуваний формат — «гг:хх». Спробуйте ще раз:")

@router.callback_query(F.data.startswith("del-not-"), StateFilter(None))
async def btn_del_not(callback: CallbackQuery, state: FSMContext):
    """
    Ask whether they are sure they want to delete the specified notification.
    """

    await callback.answer()

    hm = callback.data.split("-")[2]
    hm_details = HEALTH_METRICS.get(hm)

    # Remove the inline keyboard.
    msg_text = Text(Bold("Видалити"), " ", hm_details.get("button_text"))
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
            "Ви впевнені, що хочете видалити сповіщення для показника "
            f"{hm_details.get('button_text')}?"
        ),
        reply_markup=get_confirmation_kb("submit-del-not").as_markup()
    )

@router.callback_query(F.data=="submit-del-not", StateFilter(ConfirmationSG.confirmation))
async def btn_submit(
    callback: CallbackQuery,
    state: FSMContext,
    scheduler: AsyncIOScheduler
):
    """
    Delete the notification.
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

    # Remove the notification
    scheduler.remove_job(f"{user_tg_id}-{hm}")

    # Let the user know that this metric was deleted
    await callback.message.answer("Сповіщення видалено")

    await state.clear()