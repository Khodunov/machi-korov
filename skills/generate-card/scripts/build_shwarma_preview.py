#!/usr/bin/env python3
"""Render the six numbered shawarma cards as a comparison sheet."""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


root = Path(__file__).resolve().parents[3]
width, height, gap, label_height = 550, 715, 18, 42
sheet = Image.new("RGB", (3 * width + 4 * gap, 2 * (height + label_height) + 3 * gap), "#eee9dd")
draw = ImageDraw.Draw(sheet)
font = ImageFont.truetype(str(root / "fonts/CCUltimatum-Bold.ttf"), 25)
labels = ['00. Исходная', '01. Цоколь', '02. Маршрутка', '03. Зима', '04. Школьники', '05. Столик']
variants = ['shwarma', 'shwarma-01-tsokol-v5', 'shwarma-02-marshrutka-v5', 'shwarma-03-zima-v5', 'shwarma-04-shkolniki-v5', 'shwarma-05-stolik-v5']
for i, label in enumerate(labels):
    x = gap + (i % 3) * (width + gap)
    y = gap + (i // 3) * (height + label_height + gap)
    draw.text((x + width / 2, y + 5), label, font=font, fill="#58100E", anchor="mt")
    card = Image.open(root / f"cards/{variants[i]}.png").convert("RGB")
    sheet.paste(card.resize((width, height), Image.Resampling.LANCZOS), (x, y + label_height))
output = root / "cards/shwarma-six-approved.jpg"
sheet.save(output, quality=95)
print(output)
