import json
import discord
import datetime
import pytz

from config import config_id, config_time_zone
from discord.ext import  tasks

kyiv = pytz.timezone(config_time_zone.kyiv_tz)
    
def setup_gambling_roles(client):
    global bot
    bot = client


@tasks.loop(minutes=1)
async def check_roles():
    # Чекаємо, поки бот буде готовий
    if not bot.is_ready():
        return

    now = datetime.datetime.now(kyiv)

    if now.hour == 12 and now.minute == 00:

        # читаємо JSON
        try:
            with open("database/UsersInGamblinng.json", "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception as e:
            print("Error reading JSON:", e)
            return

        last_spin = data.get("lastSpinDate")
        if last_spin:
            try:
                last_spin_date = datetime.datetime.strptime(last_spin, "%Y-%m-%d").date()
            except Exception as e:
                print("Error parsing lastSpinDate:", e)
                return

            # якщо вже крутили сьогодні
            if last_spin_date == now.date():
                return

        # отримуємо гільдію та канал
        guild = bot.get_guild(config_id.id_guild)
        if not guild:
            print("Guild not found")
            return

        channel = guild.get_channel(config_id.id_main_chat_channel)
        if not channel:
            print("Channel not found")
            return

        # отримуємо ролі
        imba_role = discord.utils.get(guild.roles, name="Імба")
        toxic_role = discord.utils.get(guild.roles, name="Токсік")

        imba_members = imba_role.members if imba_role else []
        toxic_members = toxic_role.members if toxic_role else []

        if imba_members or toxic_members:
            embed = discord.Embed(
                title="⚠️ Ролі ще не прибрані",
                description="Ролі все ще у старих користувачів:",
                color=discord.Color.blue()  # синя смужка
            )

            if imba_members:
                embed.add_field(
                    name="Імба",
                    value="\n".join(member.mention for member in imba_members),
                    inline=False
                )

            if toxic_members:
                embed.add_field(
                    name="Токсик",
                    value="\n".join(member.mention for member in toxic_members),
                    inline=False
                )

            await channel.send(embed=embed)
         

@check_roles.before_loop
async def before_check_roles():
    await bot.wait_until_ready()