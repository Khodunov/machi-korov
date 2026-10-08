"""Build airport contact sheets and downloadable paired PNG bundle."""
import json
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
from PIL import Image, ImageDraw, ImageFont
ROOT = Path(__file__).resolve().parents[1]
items = json.loads((ROOT/'references/airports/manifest.json').read_text())
font = ImageFont.truetype(str(ROOT/'fonts/CCUltimatum-Bold.ttf'), 21)
fronts = Image.new('RGB', (1800, 650), '#f7f4ec')
pairs = Image.new('RGB', (1200, 470*len(items)), '#f7f4ec')
for i,j in enumerate(items):
 slug = j['slug']
 front = Image.open(ROOT/f'cards/{slug}.png').convert('RGB'); assert front.size == (1024,1536)
 back = Image.open(ROOT/f'card-backs/{slug}.png').convert('RGB'); assert back.size == front.size
 small = front.resize((360,540),Image.Resampling.LANCZOS)
 fronts.paste(small,(i*360,60))
 ImageDraw.Draw(fronts).text((i*360+14,20),j['name'].split(' — ')[0],font=font,fill='#473424')
 for k,im in enumerate([front,back]):
  im.thumbnail((285,428));pairs.paste(im,(k*300,i*470+35))
 ImageDraw.Draw(pairs).text((610,i*470+180),j['name'],font=font,fill='#473424')
fronts.save(ROOT/'cards/airports-five-preview.jpg',quality=94)
pairs.save(ROOT/'cards/airports-pairs-review.jpg',quality=90)
with ZipFile(ROOT/'cards/airports-five-cards.zip','w',ZIP_DEFLATED) as z:
 for j in items:
  for folder in ['cards','card-backs']:
   p=ROOT/f"{folder}/{j['slug']}.png";z.write(p,f"{'fronts' if folder=='cards' else 'backs'}/{p.name}")
