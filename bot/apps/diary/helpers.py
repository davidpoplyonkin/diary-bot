from aiogram.types import Message
from aiogram.fsm.context import  FSMContext

from globals import HEALTH_METRICS
from ..core.markup import get_cancel_btn

async def get_metric(message: Message, state: FSMContext, prompt: str | None = None):
    """
    Asks the user to enter the current metric value.
    """

    # Get the current health metric.
    state_data = await state.get_data()
    hm = state_data.get("hm")

    hm_details = HEALTH_METRICS.get(hm)

    if prompt is None:
        prompt = hm_details.get("prompt")

    return await message.answer(
        text=prompt,
        reply_markup=get_cancel_btn().as_markup(),
    )
