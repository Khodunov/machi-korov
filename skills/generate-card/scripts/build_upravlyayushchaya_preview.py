#!/usr/bin/env python3
"""Render the six numbered management-company cards as a comparison sheet."""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


root = Path(__file__).resolve().parents[3]
width, height, gap, label_height = 550, 715, 18, 42
sheet = Image.new("RGB", (3 * width + 4 * gap, 2 * (height + label_height) + 3 * gap), "#eee9dd")
draw = ImageDraw.Draw(sheet)
font = ImageFont.truetype(str(root / "fonts/CCUltimatum-Bold.ttf"), 25)
labels = ["1. Диспетчерша", "2. Объявления", "3. Старая дверь", "4. Цоколь", "5. Видеоконтроль", "6. Бывший детсад"]
variants = ["1-final", "2", "3", "4", "5-revised", "6"]
for i, label in enumerate(labels):
    x = gap + (i % 3) * (width + gap)
    y = gap + (i // 3) * (height + label_height + gap)
    draw.text((x + width / 2, y + 5), label, font=font, fill="#17361A", anchor="mt")
    card = Image.open(root / f"cards/upravlyayushchaya-kompaniya-v{variants[i]}.png").convert("RGB")
    sheet.paste(card.resize((width, height), Image.Resampling.LANCZOS), (x, y + label_height))
output = root / "cards/upravlyayushchaya-kompaniya-six-variants.jpg"
sheet.save(output, quality=95)
print(output)
