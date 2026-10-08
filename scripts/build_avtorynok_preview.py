"""Build a proportion-preserving comparison sheet of current Autorынок cards."""
import json
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageOps
root=Path(__file__).resolve().parents[1]
c=next(c for c in json.loads((root/'cards-config.json').read_text())['cards'] if c['slug']=='avtorynok')
labels=['Торг с другом','Проверка колеса','Зимний запуск','Осмотр с подборщиком','Проверка магнитом','Запчасти в придачу']
w,h,gap,lh=512,768,20,44
sheet=Image.new('RGB',(3*w+4*gap,2*(h+lh)+3*gap),'#eee9dd')
draw=ImageDraw.Draw(sheet);font=ImageFont.truetype(str(root/'fonts/CCUltimatum-Bold.ttf'),25)
for i,(slug,label) in enumerate(zip(c['art_variants'],labels)):
 x=gap+i%3*(w+gap);y=gap+i//3*(h+lh+gap)
 draw.text((x+w/2,y+5),f'{i+1}. {label}',font=font,fill='#17361A',anchor='mt')
 with Image.open(root/f'cards/{slug}.png') as im: sheet.paste(ImageOps.pad(im.convert('RGB'),(w,h),method=Image.Resampling.LANCZOS,color='#eee9dd'),(x,y+lh))
sheet.save(root/'cards/avtorynok-six-variants.jpg',quality=95)
