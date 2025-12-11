from aiogram import Router, F, Bot
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.utils.formatting import Text, Bold, as_list

from .markup import get_health_metrics_kb, get_confirmation_kb
from .helpers import get_metric
from globals import HEALTH_METRICS, ADMIN_TG_ID

router = Router()

# Create a state for each health metric
health_metrics_sg = type(
    "HealthMetricsSG",
    (StatesGroup,),
    {hm: State() for hm in HEALTH_METRICS.keys()},
)

class ConfirmationSG(StatesGroup):
    confirmation = State()

@router.message(Command("enter"), StateFilter(None))
async def cmd_enter(message: Message):
    """
    Answers to /enter with a list of available health metrics.
    """

    await message.answer(
        "Choose one of the following health metrics:",
        reply_markup=get_health_metrics_kb().as_markup()
    )

@router.callback_query(F.data.startswith("enter-"), StateFilter(None))
async def btn_metric(callback: CallbackQuery, state: FSMContext):
    """
    Asks the user to enter the first of a sequence of related metrics.
    """

    await callback.answer()

    hm = callback.data.split("-")[1] # callback.data ~ "enter-sbp"
    hm_details = HEALTH_METRICS[hm]

    # Remove the inline keyboard.
    msg_text = Text(Bold(hm_details.get("button_text")))
    msg_kwargs = msg_text.as_kwargs()
    msg_kwargs["reply_markup"] = None
    await callback.message.edit_text(**msg_kwargs)

    # Remove the inline keyboard.
    callback.message.edit_text(
        text=hm_details.get("button_text"),
        reply_markup=None
    )

    # Store the current metric name.
    await state.update_data(hm=hm)

    # Set the state of waiting for the first metric value.
    await state.set_state(getattr(health_metrics_sg, hm))

    # Ask the user to enter the first metric value.
    ans = await get_metric(callback.message, state)

    # Record the answer ID in order to then remove the attached cancel
    # button
    await state.update_data(
        ans_msg_id=ans.message_id,
        ans_chat_id=ans.chat.id,
    )

@router.message(StateFilter(health_metrics_sg))
async def msg_metric(message: Message, state: FSMContext, bot: Bot):
    """
    Saves the value the user entered and proceeds with the next metric
    if there is one.
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
        # If the message was sent long ago, it would be impossible to
        # edit it.
        pass

    hm = state_data.get("hm")
    hm_details = HEALTH_METRICS.get(hm)

    # Validate user input.
    try:
        val = float(message.text)
        input_valid = True
    except:
        input_valid = False

    if not input_valid:
        # Don't change the state and ask the user to enter a valid
        # number.
        ans = await get_metric(message, state, "Not a number. Try again:")

        # Record the answer ID in order to then remove the attached cancel
        # button
        await state.update_data(
            ans_msg_id=ans.message_id,
            ans_chat_id=ans.chat.id,
        )

        return
    
    # Save user input.
    await state.update_data(**{f"val_{hm}": val})

    # If this wasn't the last metric in a sequence
    if hm_details.get("next"):
        # Change the current health metric
        await state.update_data(hm=hm_details.get("next"))

        # Set the state of waiting for the next metric value.
        await state.set_state(getattr(health_metrics_sg, hm))

        # Ask the user to enter the next value.
        ans = await get_metric(message, state)

        # Record the answer ID in order to then remove the attached cancel
        # button
        await state.update_data(
            ans_msg_id=ans.message_id,
            ans_chat_id=ans.chat.id,
        )
    else:
        # Set the state of waiting for confirmation.
        await state.set_state(ConfirmationSG.confirmation)

        # Updating `state_data` since it doesn't contain the last answer.
        state_data = await state.get_data()

        summary_lines = [Text(Bold("Doublecheck:"))]
     
        for k, v in state_data.items():
            if k.startswith("val_"):
                hm = k[4:] # Discard "val_"
                hm_details = HEALTH_METRICS.get(hm)

                summary_lines.append(f"{hm_details.get('name')} - {v}")

        msg_text = as_list(*summary_lines)
        msg_kwargs = msg_text.as_kwargs()
        msg_kwargs["reply_markup"] = get_confirmation_kb().as_markup()
        await message.answer(**msg_kwargs)

@router.callback_query(F.data=="cancel-hm", StateFilter(health_metrics_sg, ConfirmationSG.confirmation))
async def btn_cancel(callback: CallbackQuery, state: FSMContext):
    """
    Interrupt the sequence of health metrics.
    """

    await callback.answer()

    # Remove the inline keyboard.
    await callback.message.edit_reply_markup(reply_markup=None)

    msg_text = Text(Bold("Cancel"))
    msg_kwargs = msg_text.as_kwargs()
    await callback.message.answer(**msg_kwargs)

    await state.clear()

@router.callback_query(F.data=="submit-hm", StateFilter(ConfirmationSG.confirmation))
async def btn_submit(callback: CallbackQuery, state: FSMContext, bot: Bot):
    """
    Submit the sequence of health metrics.
    """

    await callback.answer()

    await callback.message.edit_reply_markup(reply_markup=None)

    state_data = await state.get_data()

    summary_lines = [Text(Bold(callback.from_user.full_name))]
     
    for k, v in state_data.items():
        if k.startswith("val_"):
            hm = k[4:] # Discard "val_"
            hm_details = HEALTH_METRICS.get(hm)

            summary_lines.append(f"{hm_details.get('name')} - {v}")

    # Send the user results to admin.
    msg_text = as_list(*summary_lines)
    msg_kwargs = msg_text.as_kwargs()
    msg_kwargs["chat_id"] = ADMIN_TG_ID
    await bot.send_message(**msg_kwargs)

    # Let the user know that this was the last metric in a sequence.
    await callback.message.answer("Done")

    await state.clear()
