import random
import requests
import discord
import os
import textwrap

from PIL import Image, ImageDraw, ImageFont
from io import BytesIO

from datetime import date
from discord import app_commands, Interaction
from .storage import save_data, load_data
from . import gambling_config 
from . import generate_image
from datetime import datetime
from zoneinfo import ZoneInfo



def register(tree: app_commands.CommandTree):
    # Команда для регистрации в гемблинге ролей
    @tree.command(name = "register_to_gambling", 
                  description="Записатись в дуже цікаву авантюру по ролу ролей на день"
                  )
    
    async def register(interaction: Interaction):
        data = load_data()
        user_id = str(interaction.user.id)

        if "userList" not in data:
            data["userList"] = []
        
        if user_id in data["userList"]:
            await interaction.response.send_message(
                "Ви вже зареєстровані",
                ephemeral=True
                )
            return
    


        await interaction.response.send_message(
            f"Вас будо додано до гемблінгу ролей, Успішних вам голодних ігор\nНехай імбувати буде сильніший"
        )

    # Команда для удаления себя из списка участников гемблинга
    @tree.command(
        name="clear_gambling",
        description="Видалити себе зі  списку учасників гемблінгу"
    )
    async def clear_gambling(interaction: Interaction):
        data = load_data()
        user_id = str(interaction.user.id)

        if "userList" not in data or user_id not in data["userList"]:
            await interaction.response.send_message(
                "Ви і так не зареєстровані в гемблінгу",
                ephemeral=True
            )
            return
        
        data["userList"].remove(user_id)
        save_data(data)

        await interaction.response.send_message(
            "Вас було видалено зі списку учасників гемблінгу"
        )

    # Команда для запуска гемблинга ролей

    
    @tree.command(
    name="spin_roles",
    description="Запустити гемблінг"
)
    async def spin_roles(interaction: Interaction):
        data = load_data()
        kyiv_time = datetime.now(ZoneInfo("Europe/Kyiv")).date()
        last_spin = data.get("lastSpinDate")

        # Проверка минимум 2 игрока
        if len(data.get("userList", [])) < 2:
            await interaction.response.send_message("❌ Потрібно мінімум 2 гравця")
            return

        # Если уже крутили сегодня — ответ через followup
    
        if last_spin == str(kyiv_time) and "imba" in data and "toxic" in data:
            imba = data.get("imba")
            toxic = data.get("toxic")
            await interaction.response.send_message(
                f"🎲 Сьогодні вже крутили!\n"
                f"💪 Імба: <@{imba}>\n"
                f"☠️ Токсик: <@{toxic}>",
                ephemeral=True
            )
            return

        # Делаем defer для долгих операций (аватарки, картинки)
        await interaction.response.defer()

        # Выбираем игроков
        imba = random.choice(data["userList"])
        toxic = random.choice([u for u in data["userList"] if u != imba])

        # Сохраняем выбор, чтобы потом можно было показать в следующий раз
        data["lastSpinDate"] = str(kyiv_time)
        data["imba"] = imba
        data["toxic"] = toxic
        save_data(data)

        # Получаем их аватарки
        imba_member = await interaction.guild.fetch_member(int(imba))
        toxic_member = await interaction.guild.fetch_member(int(toxic))

        imba_avatar_url = str(imba_member.display_avatar.url)
        toxic_avatar_url = str(toxic_member.display_avatar.url)

        # Выдача ролей
        imba_role = interaction.guild.get_role(gambling_config.role_imba)
        toxic_role = interaction.guild.get_role(gambling_config.role_toxic)

        # Удаляем старые роли
        for member in interaction.guild.members:
            if imba_role in member.roles:
                await member.remove_roles(imba_role)
            if toxic_role in member.roles:
                await member.remove_roles(toxic_role)

        # Выдаем новые роли
        await imba_member.add_roles(imba_role)
        await toxic_member.add_roles(toxic_role)

        # --- Функция выбора текста ---
        def get_answer(user_id, category):
            answers = gambling_config.user_answers.get(category, {})
            use_default = random.random() < 0.15  # 15% шанс использовать дефолтные ответы
            if use_default:
                pool = answers.get("default", ["Тут немає відповіді"])
            else:
                pool = answers.get(str(user_id), answers.get("default", ["Тут немає відповіді"]))
            return random.choice(pool)

        imba_text = get_answer(imba, "imba_answer")
        toxic_text = get_answer(toxic, "toxic_answer")

        # Создаем картинки
        generate_image.create_card(generate_image.imba_template, imba_avatar_url, imba_text, "imba_result.png", imba_member.display_name)
        generate_image.create_card(generate_image.toxic_template, toxic_avatar_url, toxic_text, "toxic_result.png", toxic_member.display_name)

        # Отправляем в Discord
        imba_file = discord.File("imba_result.png")
        toxic_file = discord.File("toxic_result.png")

        await interaction.followup.send(
            f"💪 Імба: <@{imba}>\n",
            file=imba_file
        ) 
        await interaction.followup.send(
            f"☠️ Токсик: <@{toxic}>",
            file=toxic_file
        )