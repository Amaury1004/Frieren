# events/voice_ping.py
import asyncio
from datetime import datetime

# Словарь: {user_id: время входа}
user_join_time = {}

PING_TIME = 18000  # время до пинга в секундах
TEXT_CHANNEL_ID = 1378468435121537169  


def setup_voice_ping(bot):
    @bot.event
    async def on_voice_state_update(member, before, after):
        # Пользователь вошёл в канал
        if after.channel and (before.channel != after.channel):
            user_join_time[member.id] = datetime.now()
            # Запускаем пинг через PING_TIME секунд
            asyncio.create_task(ping_user_after(member, after.channel, PING_TIME, bot))
        
        # Пользователь вышел из канала
        if before.channel and (before.channel != after.channel):
            user_join_time.pop(member.id, None)


async def ping_user_after(member, voice_channel, delay, bot):
    await asyncio.sleep(delay)
    if member.id in [m.id for m in voice_channel.members]:
        text_channel = bot.get_channel(TEXT_CHANNEL_ID)
        if text_channel:
            print()
           #await text_channel.send(f"{member.mention}, ти вже {delay} годин в каналі {voice_channel.name}! Навіть я стільки не сиджу над фоліантами!")
