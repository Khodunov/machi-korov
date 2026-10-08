"""Render current base-set variants and collect one full-resolution sheet per type."""

import json
import math
import os
from pathlib import Path
import subprocess
import zipfile

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'cards/base-set'


def main():
    cards = [c for c in json.loads((ROOT / 'cards-config.json').read_text())['cards']
             if c['set'] == 'base']
    commands = [ROOT / f'card-commands/{v}.sh' for c in cards for v in c['art_variants']]
    missing = [str(p) for p in commands if not p.is_file()]
    if missing:
        raise FileNotFoundError('\n'.join(missing))
    OUT.mkdir(parents=True, exist_ok=True)
    env = dict(os.environ, PATH=f"{ROOT / '.venv/bin'}:{os.environ['PATH']}")
    for i, command in enumerate(commands, 1):
        subprocess.run(['bash', '-n', str(command)], check=True, cwd=ROOT)
        result = subprocess.run(['bash', str(command)], cwd=ROOT, env=env,
                                capture_output=True, text=True)
        if result.returncode:
            raise RuntimeError(f'{command.name}\n{result.stdout}\n{result.stderr}')
        print(f'[{i}/{len(commands)}] {command.stem}', flush=True)

    font = ImageFont.truetype(str(ROOT / 'fonts/CCUltimatum-Bold.ttf'), 54)
    manifest = []
    for card in cards:
        variants = card['art_variants']
        cols = 4 if len(variants) > 6 else 3
        rows = math.ceil(len(variants) / cols)
        w, h, gap, header = 1024, 1536, 32, 130
        sheet = Image.new('RGB', (cols * (w + gap) + gap,
                                 rows * (h + gap) + gap + header), '#eee9dd')
        draw = ImageDraw.Draw(sheet)
        draw.text((gap, 32), f"{card['title']} · {len(variants)} вариантов",
                  font=font, fill='#302d28')
        for i, variant in enumerate(variants):
            with Image.open(ROOT / f'cards/{variant}.png') as source:
                if source.size != (w, h):
                    raise ValueError(f'{variant}: unexpected dimensions {source.size}')
                image = source.convert('RGBA')
                sheet.paste(image, (gap + i % cols * (w + gap),
                                   header + gap + i // cols * (h + gap)), image)
        filename = f"{card['slug']}.jpg"
        sheet.save(OUT / filename, quality=95, subsampling=0)
        manifest.append({'title': card['title'], 'image': filename, 'variants': variants})
    (OUT / 'manifest.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n')
    with zipfile.ZipFile(ROOT / 'cards/base-set-all-variations.zip', 'w', zipfile.ZIP_DEFLATED) as archive:
        for item in manifest:
            archive.write(OUT / item['image'], item['image'])
        archive.write(OUT / 'manifest.json', 'manifest.json')
    print(f"Saved {len(cards)} sheets / {len(commands)} variants to {OUT}")


if __name__ == '__main__':
    main()
