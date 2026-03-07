from discord import app_commands, Interaction
import random 

def register(tree):
    @tree.command(name="roll", description="Кинь кубик від 1 до 6ажаного числа")
    async def roll_command(interaction: Interaction, number: int):
        if number < 1:
            await interaction.response.send_message(
            "Введене число має бути більше за 0!", ephemeral=True)
            return
        result = random.randint(1, number)

        if result == number:
            await interaction.response.send_message(
                f"🔥 Вау! Ви кинули максимальне число {result} з {number}! Це критична вдача."
            )
        elif result == 1:
            await interaction.response.send_message(
                f"💀 Випала 1 з {number}. Повний провал дії.")
        elif number > 20 and result <= 5:
            await interaction.response.send_message(
                f"😬 Невдало… Ви кинули {result} з {number}")
        elif number > 20 and result >= number - 5:
            await interaction.response.send_message(
                f"✨ Майже ідеально! Ви кинули {result} з {number}")
        else:
            await interaction.response.send_message(
                f"🎲 Ви кинули кубик і випало {result} з {number}")