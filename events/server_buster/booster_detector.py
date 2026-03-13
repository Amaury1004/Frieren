import os

import discord 

from  config import config_id
from core import bot

boost_image = "Assets/Marsil.png"

boost_count = {}

@bot.event
async def on_member_update(before, after):

    channel = bot.get_channel(config_id.id_main_chat_channel)

    if not channel:
        return

    # 🚀 НОВИЙ БУСТ
    if before.premium_since is None and after.premium_since is not None:

        boost_count[after.id] = boost_count.get(after.id, 0) + 1

        embed = discord.Embed(
            title="🚀 SERVER BOOST!",
            description=f"{after.mention} щойно бустнув сервер!",
            color=discord.Color.purple()
        )

        embed.add_field(
            name="💎 Бустів від користувача",
            value=boost_count[after.id],
            inline=False
        )

        embed.set_footer(text="Дякуємо за підтримку сервера ❤️")

        file = discord.File(boost_image, filename="boost.png")
        embed.set_image(url="attachment://boost.png")

        await channel.send(embed=embed, file=file)

    # ❌ БУСТ ЗАКІНЧИВСЯ
    if before.premium_since is not None and after.premium_since is None:

        embed = discord.Embed(
            title="💔 Boost закінчився",
            description=f"{after.mention} більше не бустить сервер. =(",
            color=discord.Color.red()
        )

        await channel.send(embed=embed)