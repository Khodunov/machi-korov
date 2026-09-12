#!/usr/bin/env python3
"""Rebuild five shawarma cards and preview from preserved image_gen originals."""
import argparse, json, os, subprocess, sys, zipfile
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
ROOT = Path(__file__).resolve().parents[1]
os.chdir(ROOT)
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--manifest', default='prompts/central-illustrations/shwarma-five-production.json')
args = parser.parse_args()
manifest = json.loads(Path(args.manifest).read_text())
prefix = manifest.get('output_prefix', 'shwarma-five-variants')
env = {**os.environ, 'PATH': str(Path(sys.executable).parent) + os.pathsep + os.environ['PATH']}
for v in manifest['variants']:
    subprocess.run([sys.executable, 'skills/generate-card/scripts/remove_light_background.py', v['source'], v['cutout']], check=True)
    subprocess.run(['bash', 'card-commands/' + v['slug'] + '.sh'], env=env, check=True)
font = ImageFont.truetype('fonts/Boingster-Regular.ttf', 26)
sheet = Image.new('RGB', (1536, 1460), '#e9edf2')
draw = ImageDraw.Draw(sheet)
for i, v in enumerate(manifest['variants']):
    card = Image.open(v['card']).convert('RGB')
    card.thumbnail((480, 660), Image.Resampling.LANCZOS)
    x, y = 24 + (i % 3)*504, 18 + (i//3)*722
    sheet.paste(card, (x+(480-card.width)//2,y))
    draw.text((x+240,y+670), f"{i+1}. {v['label']}", font=font, fill='#183956', anchor='mt')
sheet.save(f'cards/{prefix}.jpg', quality=95)
with zipfile.ZipFile(f'cards/{prefix}.zip', 'w', zipfile.ZIP_DEFLATED) as archive:
    for v in manifest['variants']:
        for p in [v['source'],v['cutout'],v['card'],'card-commands/'+v['slug']+'.sh']:
            archive.write(p)
    archive.write(args.manifest)
    archive.write(f'cards/{prefix}.jpg')
print('Saved five cards, comparison sheet, and archive.')
