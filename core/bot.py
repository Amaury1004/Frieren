import discord
from discord import app_commands
from core.intents import get_intents


if not discord.opus.is_loaded():
    discord.opus.load_opus("/opt/homebrew/lib/libopus.dylib")
    
class MyBot(discord.Client):
    def __init__(self):
        super().__init__(intents=get_intents())
        self.tree = app_commands.CommandTree(self)

