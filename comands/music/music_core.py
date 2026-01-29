import yt_dlp
import discord
import asyncio

YTDL_OPTIONS = {
    "format": "bestaudio/best",
    "quiet": True,
    "noplaylist": True,
    "extractor_args": {
        "youtube": {
            "player_client": ["android"]
        }
    }
}

FFMPEG_OPTIONS = {
    "before_options": "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5",
    "options": "-vn"
}

ytdl = yt_dlp.YoutubeDL(YTDL_OPTIONS)

async def play_youtube(vc, url):
    loop = asyncio.get_event_loop()

    data = await loop.run_in_executor(
        None,
        lambda: ytdl.extract_info(url, download=False)
    )

    audio_url = data["url"]

    source = discord.FFmpegPCMAudio(
        audio_url,
        executable="/opt/homebrew/bin/ffmpeg",
        **FFMPEG_OPTIONS
    )

    vc.play(source)