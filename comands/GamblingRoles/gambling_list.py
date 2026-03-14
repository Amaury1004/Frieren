from discord import app_commands, Interaction, Embed
from .storage import load_data

def register(tree: app_commands.CommandTree):

    @tree.command(name="gambling_list", description="Показати хто скільки раз був імбою і токсиком")
    async def gambling_list(interaction: Interaction):

        data = load_data()

        if "counterImba" not in data or "counterToxic" not in data:
            await interaction.response.send_message(
                "Дані про гемблінг ролей ще не зібрані",
                ephemeral=True
            )
            return

        guild = interaction.guild

        # сортуємо по кількості
        sorted_imba = sorted(data["counterImba"].items(), key=lambda x: x[1], reverse=True)
        sorted_toxic = sorted(data["counterToxic"].items(), key=lambda x: x[1], reverse=True)

        imba_lines = []
        toxic_lines = []

        for user_id, count in sorted_imba:
            member = guild.get_member(int(user_id))
            name = member.display_name if member else f"User {user_id}"
            imba_lines.append(f"{name} — **{count}**")

        for user_id, count in sorted_toxic:
            member = guild.get_member(int(user_id))
            name = member.display_name if member else f"User {user_id}"
            toxic_lines.append(f"{name} — **{count}**")

        embed1 = Embed(
            color=0xffffff  # біла смужка
        )

        embed1.add_field(
            name="👑 Імба",
            value="\n".join(imba_lines) if imba_lines else "Немає даних",
            inline=False
        )

        embed2 = Embed(
            color=0xffffff  # біла смужка
        )
        embed2.add_field(
            name="☠️ Токсик",
            value="\n".join(toxic_lines) if toxic_lines else "Немає даних",
            inline=False
        )

        # аватарка топ імби
        if sorted_imba:
            top_member = guild.get_member(int(sorted_imba[0][0]))
            if top_member:
                embed1.set_thumbnail(url=top_member.display_avatar.url)
        if sorted_toxic:
            top_member = guild.get_member(int(sorted_toxic[0][0]))
            if top_member:
                embed2.set_thumbnail(url=top_member.display_avatar.url)
        

        await interaction.response.send_message("🎲 Гемблінг ролей — статистика")

        await interaction.followup.send(embed=embed1)
        await interaction.followup.send(embed=embed2)