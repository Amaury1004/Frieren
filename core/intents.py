import discord

def get_intents():
    intents = discord.Intents.default()
    intents.members = True
    intents.reactions = True
    intents.guilds = True
    intents.voice_states = True
    return intents