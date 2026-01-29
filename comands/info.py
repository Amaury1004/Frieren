import config

def register(tree):

    @tree.command(name="info", description="Інформація про бота")
    async def info(interaction):
        await interaction.response.send_message(config.info)
