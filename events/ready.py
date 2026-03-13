import discord
from moduls.new_day.play_new_day import daily_task
from . import check_gambling_roles
from config import config_id
from core import bot


async def handle_ready(bot, member=None):
    print(f"Logged in as {bot.user}")
    await bot.tree.sync()

    # запуск daily task
    daily_task.bot = bot
    daily_task.start()

    # передаем бот в систему ролей
    check_gambling_roles.setup_gambling_roles(bot)

    # запускаем loop
    if not check_gambling_roles.check_roles.is_running():
        check_gambling_roles.check_roles.start()

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
        activity=discord.Game(name="Шукає фоліанти")
        )
   
    