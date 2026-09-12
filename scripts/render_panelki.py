#!/usr/bin/env python3
"""Recreate ten panelka cutouts, cards, and a numbered preview from saved art."""
import argparse
import json
import os
import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--manifest', default='prompts/central-illustrations/panelki-production.json')
    parser.add_argument('--allow-incomplete', action='store_true', help='Render available cards and clearly name the partial preview.')
    args = parser.parse_args()
    os.chdir(ROOT)
    manifest = json.loads(Path(args.manifest).read_text())
    variants = manifest['variants']
    missing = [v['source'] for v in variants if not Path(v['source']).is_file()]
    if missing and not args.allow_incomplete:
        raise SystemExit('Missing generated source artwork: ' + ', '.join(missing))
    available = [(i, v) for i, v in enumerate(variants) if Path(v['source']).is_file()]
    env = {**os.environ, 'PATH': str(Path(sys.executable).parent) + os.pathsep + os.environ['PATH']}
    for _, v in available:
        command = [sys.executable, 'skills/generate-card/scripts/remove_light_background.py', v['source'], v['cutout']]
        for x, y in v.get('background_seeds', []):
            command += ['--background-seed', str(x), str(y)]
        for region in v.get('background_regions', []):
            command += ['--background-region', *map(str, region)]
        subprocess.run(command, check=True)
        subprocess.run(['bash', f"card-commands/{v['slug']}.sh"], env=env, check=True)
    tile_w, tile_h, gap = 440, 604, 18
    columns = 5 if len(available) == 10 else 3
    rows = (len(available) + columns - 1) // columns
    sheet = Image.new('RGB', (columns * tile_w + (columns + 1) * gap, rows * tile_h + (rows + 1) * gap), '#e9edf2')
    draw = ImageDraw.Draw(sheet)
    font = ImageFont.truetype('fonts/Boingster-Regular.ttf', 20)
    labels = ['Ковёр', 'Лебеди', 'Огород', 'Утепление', 'Космодром', 'Балконы', 'Дом-корабль', 'Сугроб', 'Мозаика', 'Тропинка']
    for slot, (i, v) in enumerate(available):
        x, y = gap + (slot % columns) * (tile_w + gap), gap + (slot // columns) * (tile_h + gap)
        card = Image.open(v['card']).convert('RGB')
        card.thumbnail((tile_w, 572), Image.Resampling.LANCZOS)
        sheet.paste(card, (x, y))
        draw.text((x + tile_w / 2, y + 582), f'{i + 1}. {labels[i]}', font=font, fill='#183956', anchor='mt')
    prefix = manifest.get('output_prefix', 'panelki')
    preview = f'cards/{prefix}-ten-variants.jpg' if not missing else f'cards/{prefix}-{len(available)}-ready.jpg'
    sheet.save(preview, quality=95)
    print(f'Rebuilt {len(available)} cards and {preview}')
    if missing:
        print('Still missing: ' + ', '.join(missing))


if __name__ == '__main__':
    main()
