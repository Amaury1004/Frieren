import discord
from config import config_id
from services.GachaCats.cats_service import cats

def register(tree):

    @tree.command(name="gacha_cat", description="Отримати котика 🐱")
    async def gacha_cat(interaction):
        if interaction.channel_id != config_id.id_cats_channel:
            await interaction.response.send_message(
                "❌ Тільки #cats",
                ephemeral=True
            )
            return

        await interaction.response.defer()
        image = await cats.fetch_image()
        await interaction.followup.send(
            file=discord.File(image, "cat.jpg")
        )
