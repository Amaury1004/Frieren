# main.py
import config
from core.bot import MyBot

# handlers (логика)
from events.ready import handle_ready
from events import voice_ping
from events.ping_message import OnMessageEvent
from events.reactions import (
    handle_reaction_add, 
    handle_reaction_remove
)
# commands
from comands import info, ask, auf, gacha_cat, good_boy
from comands.music import music_play

bot = MyBot()

# ================= EVENTS =================


OnMessageEvent(bot)
@bot.event
async def on_ready():
    await handle_ready(bot)


@bot.event
async def on_raw_reaction_add(payload):
    await handle_reaction_add(bot, payload)


@bot.event
async def on_raw_reaction_remove(payload):
    await handle_reaction_remove(bot, payload)

voice_ping.setup_voice_ping(bot)

# ================= COMMANDS =================

info.register(bot.tree)
ask.register(bot.tree)
auf.register(bot.tree)
gacha_cat.register(bot.tree)
good_boy.register(bot.tree)
music_play.register(bot.tree)


# ================= RUN =================

bot.run(config.TOKEN)