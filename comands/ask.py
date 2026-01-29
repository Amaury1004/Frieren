# commands/ask.py
from discord import app_commands, Interaction
import config


def register(tree: app_commands.CommandTree):

    @tree.command(name="ask", description="Задай мені питання")
    @app_commands.describe(question="Твоє питання для бота")
    async def ask_command(interaction: Interaction, question: str):

        if interaction.channel_id == config.id_cats_channel:
            await interaction.response.send_message(
                "❌ Цю команду не можна використовувати в каналі #cats",
                ephemeral=True
            )
            return

        response = (
            f"Ти запитав: {question}\n"
            f"Я ще вчуся відповідати 😅"
        )
        await interaction.response.send_message(response)
