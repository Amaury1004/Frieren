import discord 
from . import music_core
import config_id

ALLOWED_CHANNELS = {
    config_id.id_elf_fm_channel,
    config_id.id_elf_poligon_chanel
}

def register(tree):
    @tree.command(name="music_play", description="Фрірен почне співати YouTube мелодії")
    async def play(interaction: discord.Interaction, url: str):
        if interaction.channel_id not in ALLOWED_CHANNELS:
            await interaction.response.send_message(
                "❌ Цю команду можна використовувати тільки в #настільні-ельфійки-fm",
                ephemeral=True
            )
            return

        if not interaction.user.voice:
            await interaction.response.send_message(
                "Зайди в голосовий канал",
                ephemeral=True
            )
            return

        await interaction.response.defer()

        vc = interaction.guild.voice_client
        if not vc:
            vc = await interaction.user.voice.channel.connect()

        await music_core.play_youtube(vc, url)

        await interaction.followup.send(f"▶️ Співаю з YouTube {url}")