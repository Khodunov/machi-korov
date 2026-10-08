"""Build the six-card preview and delivery archive from rendered casino cards."""
from pathlib import Path
import json
from zipfile import ZipFile, ZIP_DEFLATED
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
variants = json.loads((ROOT / 'references/kazino/manifest.json').read_text())
preview = Image.new('RGB', (1260, 1360), '#eee8dd')
draw = ImageDraw.Draw(preview)
font = ImageFont.truetype(str(ROOT / 'fonts/CCUltimatum-Bold.ttf'), 23)
for i, variant in enumerate(variants):
    card = Image.open(ROOT / 'cards' / (variant['slug'] + '.png')).convert('RGB')
    assert card.size == (1024, 1536), card.size
    card.thumbnail((400, 600))
    x, y = 10 + i % 3 * 420, 15 + i // 3 * 675
    preview.paste(card, (x, y))
    draw.text((x, y + 612), f"{i + 1}. {variant['title']}", font=font, fill='#332b25')
preview.save(ROOT / 'cards/kazino-six-cards.jpg', quality=94)
with ZipFile(ROOT / 'cards/kazino-six-cards.zip', 'w', ZIP_DEFLATED) as archive:
    archive.write(ROOT / 'icons/gambling-chip.png', 'icons/gambling-chip.png')
    for variant in variants:
        slug = variant['slug']
        for folder, ext in [('cards', '.png'), ('buildings', '.png'), ('prompts/central-illustrations', '.json'), ('card-commands', '.sh')]:
            path = ROOT / folder / (slug + ext)
            archive.write(path, path.relative_to(ROOT))
    for path in [ROOT / 'cards/kazino-six-cards.jpg', *sorted((ROOT / 'references/kazino').glob('*'))]:
        archive.write(path, path.relative_to(ROOT))
print(ROOT / 'cards/kazino-six-cards.zip')
