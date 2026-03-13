import discord
import random
from  .ping_config import user_answers, default_answers
from config import config_id

class OnMessageEvent:
    def __init__(self, bot: discord.Client):
        self.bot = bot
        self.register()


    def register(self):
        @self.bot.event
        async def on_message(message: discord.Message):
            if message.author.bot:
                return
            if message.channel.id == config_id.id_minecraft_chat_channel:
                 return
            if self.bot.user in message.mentions:

                username = message.author.display_name
                response = user_answers.get(message.author.id, None)

                #if response:
                #       await message.channel.send(random.choice(response))

                #else:
                #    await message.channel.send(random.choice(default_answers).format(username))