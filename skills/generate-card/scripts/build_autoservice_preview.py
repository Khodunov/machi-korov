#!/usr/bin/env python3
"""Render the six numbered auto-service cards as a comparison sheet."""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


root = Path(__file__).resolve().parents[3]
width, height, gap, label_height = 550, 715, 18, 42
sheet = Image.new("RGB", (3 * width + 4 * gap, 2 * (height + label_height) + 3 * gap), "#eee9dd")
draw = ImageDraw.Draw(sheet)
font = ImageFont.truetype(str(root / "fonts/CCUltimatum-Bold.ttf"), 25)
labels = ['00. Исходный', '01. У Петровича', '02. Пацаны', '03. Первый снег', '05. Малярка', '07. Газель в рейс']
variants = ['autoservice', 'autoservice-01-petrovich', 'autoservice-02-patsany', 'autoservice-03-pervyy-sneg', 'autoservice-05-malyarka', 'autoservice-07-gazel']
for i, label in enumerate(labels):
    x = gap + (i % 3) * (width + gap)
    y = gap + (i // 3) * (height + label_height + gap)
    draw.text((x + width / 2, y + 5), label, font=font, fill="#17361A", anchor="mt")
    card = Image.open(root / f"cards/{variants[i]}.png").convert("RGB")
    sheet.paste(card.resize((width, height), Image.Resampling.LANCZOS), (x, y + label_height))
output = root / "cards/autoservice-six-variants.jpg"
sheet.save(output, quality=95)
print(output)
