from discord import app_commands, Interaction
from .storage import load_data, save_data

def register(tree: app_commands.CommandTree):

    @tree.command(
        name="add_work_place",
        description="Додати місце, куди ти подав резюме"
    )
    async def add_work_place(interaction: Interaction, team: str):
        data = load_data()
        user_id = str(interaction.user.id)

        if user_id not in data:
            data[user_id] = []

        if team in data[user_id]:
            await interaction.response.send_message(
                f"❗ Ти вже подавався в **{team}**",
                ephemeral=True
            )
            return

        data[user_id].append(team)
        save_data(data)

        await interaction.response.send_message(
            f"✅ Резюме додано: **{team}**"
        )

    @tree.command(
        name="work_places",
        description="Показати всі місця, куди ти подавався"
    )
    async def work_places(interaction: Interaction):
        data = load_data()
        user_id = str(interaction.user.id)

        if user_id not in data or not data[user_id]:
            await interaction.response.send_message(
                "📭 Ти ще нікуди не подавався",
                ephemeral=True
            )
            return

        text = "\n".join(f"• {team}" for team in data[user_id])
        await interaction.response.send_message(
            f"📄 **Твої заявки:**\n{text}"
        )