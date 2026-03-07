import discord
import pytz
import random

from discord.ext import tasks
from datetime import datetime

from core.bot import MyBot
from .config_day import wish_list_day, wish_list_weekly

import config.config_id as config_id


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
    wish_on_day = random.choice(wish_list_day)

    if channel:
        await channel.send(
            f"✨Богиня вітає вас...і повідомляє про новий день.\n"
            f"Бажаю вам сьогодні **{wish_on_day}**"
        )


async def send_weekly_message(self, channel_id: int = config_id.id_main_chat_channel):
    channel = self.get_channel(channel_id)
    wish_on_weekly = random.choice(wish_list_weekly)

    if channel:
        await channel.send("Аааааа, Иииииии, а я ще і розробці, Ня пока")


@tasks.loop(minutes=1)
async def daily_task():
    tz = pytz.timezone("Europe/Kiev")
    now = datetime.now(tz)

    # проверяем, что время 00:00
    if now.hour == 0 and now.minute == 0:
        bot = daily_task.bot  # ссылка на бот
        await join_and_play(bot, config_id.id_voice_general)
        await send_daily_message(bot)

    if now.weekday() == 0 and now.hour == 0 and now.minute == 0:
        bot = daily_task.bot
        await join_and_play(bot, config_id.id_voice_general)