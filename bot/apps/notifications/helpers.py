from globals import HEALTH_METRICS

async def notify(user_tg_id, metric, time):
    # Bot is non-serializible, so can't pass it as an argument
    from main import bot

    hm_details = HEALTH_METRICS.get(metric)

    await bot.send_message(
        chat_id=user_tg_id,
        text=f"🔔 Час вимірювання: {hm_details.get('button_text')}"
    )