import discord
from discord.ext import tasks
import pytz
from datetime import datetime
from core.bot import MyBot


import config_id

async def play_new_day(vc: discord.VoiceClient):
    source = discord.FFmpegPCMAudio(
        "Assets/audio/new_day.mp3",
        executable="/opt/homebrew/bin/ffmpeg",
        options="-vn"
    )
    vc.play(source)

async def join_and_play(bot: MyBot, channel_id: int):
    guild = bot.get_guild(config_id.id_guild)  # ID сервера
    voice_channel = guild.get_channel(channel_id)
    if not voice_channel:
        return

    vc = guild.voice_client
    if vc:
        if vc.channel != voice_channel:
            await vc.move_to(voice_channel)
    else:
        vc = await voice_channel.connect(timeout=20)

    await play_new_day(vc)
async def send_daily_message(self, channel_id: int = config_id.id_main_chat_channel):
    channel = self.get_channel(channel_id)
    if channel:
        await channel.send("✨Богиня вітає вас...і повідомляє про новий день ")

@tasks.loop(minutes=1)
async def daily_task():
    tz = pytz.timezone("Europe/Kiev")
    now = datetime.now(tz)
    # проверяем, что время 00:00
    if now.hour == 14 and now.minute == 29:
        bot = daily_task.bot  # ссылка на бот
        await join_and_play(bot, config_id.id_voice_general)
        await send_daily_message(bot)