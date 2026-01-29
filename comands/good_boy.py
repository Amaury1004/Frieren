import discord
from config import config_id

def register(tree):
    
    @tree.command(name="new_day", description="Богиня відвідає тебе...і повідомить про новий день ")
    async def good_boy_command(interaction: discord.Interaction):

        if interaction.channel_id == config_id.id_cats_channel:
            await interaction.response.send_message(
                "❌ Цю команду не можна використовувати тут",
                ephemeral=True
            )
            return

        if not interaction.user.voice:
            await interaction.response.send_message(
                "Людисько, ти повинен бути в голосовому каналі щоб викликати богиню!",
                ephemeral=True
            )
            return
        voice_channel = interaction.user.voice.channel
        vc = interaction.guild.voice_client
        if not vc:
            vc = await voice_channel.connect()

        # если бот уже играет — стоп
        if vc:
            if vc.channel != voice_channel:
                await vc.move_to(voice_channel)
        else:
            vc = await voice_channel.connect(timeout=20)
        # ▶️ MP3
        source = discord.FFmpegPCMAudio(
            "Assets/audio/new_day.mp3",  # путь к файлу
            executable="/opt/homebrew/bin/ffmpeg",
            options="-vn"
        )

        vc.play(source)

        await interaction.response.send_message(
            "✨ Богиня задоволена…"
        )


        