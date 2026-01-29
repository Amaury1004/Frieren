import discord
import config
from moduls.new_day.play_new_day import daily_task

async def handle_ready(bot):
    print(f"Logged in as {bot.user}")
    await bot.tree.sync()
    daily_task.bot = bot  # передаем объект бота в таск
    daily_task.start()

    #channel = bot.get_channel(config.ID_WELCOME_CHANNEL)
    #if not channel:
    #    print("❌ Welcome channel not found")
    #    return

    #embed = discord.Embed(
    #    title="🌸 Ласкаво просимо!",
    #    description=config.welcome_Description,
    #    color=0x9b59b6
    #)
    #embed.set_footer(text="Обери свою роль нижче ✨")

    await bot.change_presence(
        activity=discord.Game(name="У любові з Максимом 💜")
    )