from discord import app_commands, Interaction
import urllib.parse
import asyncio

def register(tree: app_commands.CommandTree):

    @tree.command(name="google", description="Пошук у Google")
    @app_commands.describe(query="Що, ти настільки лінивий шо гуглиш тут ?")

    async def google(interaction: Interaction, query: str):

        search = urllib.parse.quote(query)

        url = f"https://www.google.com/search?q={search}"

        await interaction.response.send_message(
            "Ти настільки лінивий, щоб гуглити тут? 🤨"
        )

        await asyncio.sleep(2)

        # друге повідомлення
        await interaction.followup.send(
            f"Ну добре, ось твій запит:\n{url}"
        )
        await asyncio.sleep(2)

        # третє повідомлення
        await interaction.followup.send(
            "Правда всі побачать, що ти гуглиш...\nТепер йди гугли там, я ж не можу відкривати браузер для тебе 😅"
        )