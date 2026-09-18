#!/usr/bin/env python3
"""Render the five numbered FSB cards as a comparison sheet."""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


root = Path(__file__).resolve().parents[3]
width, height, gap, label_height = 550, 715, 18, 42
sheet = Image.new("RGB", (3 * width + 4 * gap, 2 * (height + label_height) + 3 * gap), "#eee9dd")
draw = ImageDraw.Draw(sheet)
font = ImageFont.truetype(str(root / "fonts/CCUltimatum-Bold.ttf"), 25)
labels = ['00. Исходная', '01. Серый корпус', '02. Колонны', '03. Кирпич', '04. Советский']
variants = ['otdel-fsb', 'otdel-fsb-01-seryy-korpus', 'otdel-fsb-02-kolonny', 'otdel-fsb-03-kirpich', 'otdel-fsb-04-sovetskiy']
for i, label in enumerate(labels):
    x = gap + (i % 3) * (width + gap)
    y = gap + (i // 3) * (height + label_height + gap)
    draw.text((x + width / 2, y + 5), label, font=font, fill="#3E1F59", anchor="mt")
    card = Image.open(root / f"cards/{variants[i]}.png").convert("RGB")
    sheet.paste(card.resize((width, height), Image.Resampling.LANCZOS), (x, y + label_height))
output = root / "cards/otdel-fsb-five-variants.jpg"
sheet.save(output, quality=95)
print(output)
