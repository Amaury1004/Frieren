from config import config_text_message

def register(tree):

    @tree.command(name="info", description="Інформація про бота")
    async def info(interaction):
        await interaction.response.send_message(config_text_message.info)
