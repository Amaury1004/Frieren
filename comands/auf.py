import os 
import random

class Wolf: 
    def random_AufWolves(self):
        auf_Folders = "AufWolves/ImageSet"
        files = os.listdir(auf_Folders)
        image = [file for file in files if file.endswith('.png')]
        return os.path.join(auf_Folders, random.choice(image))
import discord
from discord import app_commands, Interaction

from config import config_id


def register(tree: app_commands.CommandTree):

    @tree.command(name="auf", description="Отримати auf 🐺")
    async def auf_command(interaction: Interaction):

        if interaction.channel_id == config_id.id_cats_channel:
            await interaction.response.send_message(
                "❌ Цю команду не можна використовувати тут",
                ephemeral=True
            )
            return

        wolves = Wolf()
        image_path = wolves.random_AufWolves()

        await interaction.response.send_message(
            file=discord.File(image_path)
        )