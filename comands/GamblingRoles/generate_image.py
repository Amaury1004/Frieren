from PIL import Image, ImageDraw, ImageFont
import requests
from io import BytesIO
import os

BASE_DIR = os.path.dirname(__file__)

imba_template = os.path.join(BASE_DIR, "..", "..", "Assets", "imba_template.png")
toxic_template = os.path.join(BASE_DIR, "..", "..", "Assets", "toxic_template.png")
font_path = os.path.join(BASE_DIR, "..","..", "Assets", "font", "timeNewRomanBold.otf")

# Перевіримо, чи файл реально існує
if not os.path.exists(font_path):
    raise FileNotFoundError(f"Шрифт не знайдено: {font_path}")

def create_card(template_path, avatar_url, text, output_path, name):
    img = Image.open(template_path).convert("RGBA")

    # скачать аватар
    response = requests.get(avatar_url)
    avatar = Image.open(BytesIO(response.content)).convert("RGBA")

    # сделать аватар круглый
    avatar = avatar.resize((440, 440))
    mask = Image.new("L", avatar.size, 0)
    draw_mask = ImageDraw.Draw(mask)
    draw_mask.ellipse((0, 0, 440, 440), fill=255)
    avatar.putalpha(mask)

    avatar_x = 280
    avatar_y = 320

    # координаты аватара 
    img.paste(avatar, (avatar_x, avatar_y), avatar)

    draw = ImageDraw.Draw(img)
    font_size = 55
    font = ImageFont.truetype(font_path, font_size)
    name_font = ImageFont.truetype(font_path, 70)

    bbox = draw.textbbox((0, 0), name, font=name_font)
    name_width = bbox[2] - bbox[0]

    avatar_center = avatar_x + 440 // 2
    name_x = avatar_center - name_width // 2
    name_y = avatar_y - 90

    draw.text(
        (name_x, name_y),
        name,
        fill="white",
        font=name_font,
        stroke_width=4,
        stroke_fill="black"
    )

    # ограничение по ширине текста
    max_width = img.width - 150*2  # 150px отступ слева и справа

    # функция для переноса текста по пикселям
    def wrap_text(text, font, max_width):
        lines = []
        for paragraph in text.split("\n"):
            words = paragraph.split()
            line = ""
            for word in words:
                test_line = f"{line} {word}".strip()
                # Используем textbbox для измерения ширины
                bbox = draw.textbbox((0, 0), test_line, font=font)
                w = bbox[2] - bbox[0]  # ширина текста
                if w <= max_width:
                    line = test_line
                else:
                    lines.append(line)
                    line = word
            lines.append(line)
        return "\n".join(lines)

    wrapped_text = wrap_text(text, font, max_width)

    # выводим текст с отступом 150px
    draw.multiline_text((150, 950), wrapped_text, fill="white", font=font, spacing=10)

    img.save(output_path)