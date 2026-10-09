#!/usr/bin/env python3
"""Rebuild all configured establishments and pair each copy with its back."""
import json
import math
import os
from pathlib import Path
import subprocess
import zipfile

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'cards/game-cards-with-backs'


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    config = json.loads((ROOT / 'cards-config.json').read_text())['cards']
    groups = [c for c in config if c['category'] in ('blue', 'green', 'red', 'purple')]
    env = dict(os.environ, PATH=f"{ROOT / '.venv/bin'}:{os.environ['PATH']}")
    manifest = []
    sources = set()
    for c in groups:
        variants = c['art_variants']
        fronts = []
        for variant in variants:
            command = ROOT / f'card-commands/{variant}.sh'
            filename = variant
            if not command.exists() and len(variants) == 1:
                command = ROOT / f"card-commands/{c['slug']}.sh"
                filename = c['slug']
            subprocess.run(['bash', '-n', str(command)], check=True, cwd=ROOT)
            result = subprocess.run(['bash', str(command)], cwd=ROOT, env=env,
                                    capture_output=True, text=True)
            if result.returncode:
                raise RuntimeError(f'{command.name}\n{result.stdout}\n{result.stderr}')
            fronts.append(f'cards/{filename}.png')
        count = c.get('copies', 6)  # Retain the provisional count from the prior deck.
        copies = []
        for i in range(count):
            starter = variants[i % len(variants)] in c.get('starter_variants', [])
            copies.append(dict(front=fronts[i % len(fronts)],
                               back='card-backs/starter-v1.png' if starter else 'card-backs/main-v6.png',
                               starter=starter))
        cols = min(count, 6)
        bands = math.ceil(count / cols)
        width, height, gap = 410, 615, 16
        sheet = Image.new('RGB', (cols * (width + gap) + gap,
                                  bands * 2 * (height + gap) + gap), '#f4f0e8')
        for i, copy in enumerate(copies):
            for side, key in enumerate(('front', 'back')):
                path = ROOT / copy[key]
                with Image.open(path) as original:
                    assert original.size == (1024, 1536), path
                    im = original.convert('RGBA').resize((width, height), Image.Resampling.LANCZOS)
                x = gap + (i % cols) * (width + gap)
                y = gap + (2 * (i // cols) + side) * (height + gap)
                sheet.paste(im, (x, y), im)
                sources.add(copy[key])
        sheet.save(OUT / f"{c['slug']}.jpg", quality=95, subsampling=0)
        manifest.append(dict(slug=c['slug'], title=c['title'], copies=count,
                             assumed_copies='copies' not in c, cards=copies))
        print(f"{c['title']}: {count}", flush=True)
    (OUT / 'manifest.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n')
    # One footer per type makes every rules layout reviewable at native scale.
    qa = Image.new('RGB', (4 * 1024, math.ceil(len(manifest) / 4) * 390), '#f4f0e8')
    for i, group in enumerate(manifest):
        card = Image.open(ROOT / group['cards'][-1]['front']).convert('RGB')
        qa.paste(card.crop((0, 1146, 1024, 1536)), ((i % 4) * 1024, (i // 4) * 390))
    qa.save(OUT / 'footers-review.jpg', quality=95)
    with zipfile.ZipFile(ROOT / 'cards/game-cards-with-backs.zip', 'w', zipfile.ZIP_DEFLATED) as archive:
        for group in manifest:
            archive.write(OUT / f"{group['slug']}.jpg", f"galleries/{group['slug']}.jpg")
        archive.write(OUT / 'manifest.json', 'manifest.json')
        for source in sorted(sources):
            archive.write(ROOT / source, source)
    print(f"Saved {sum(g['copies'] for g in manifest)} cards in {len(manifest)} galleries")


if __name__ == '__main__':
    main()
