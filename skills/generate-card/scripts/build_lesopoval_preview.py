from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
root=Path(__file__).resolve().parents[3]
variants=['lesopoval', 'lesopoval-01-dvuruchnaya-pila-v2', 'lesopoval-02-pilorama-v2', 'lesopoval-03-trelevochnik-v2', 'lesopoval-04-stalinskiy-lespromkhoz-v2', 'lesopoval-05-uzkokoleyka-v2']
w,h,g,lh=550,715,18,42
sheet=Image.new('RGB',(3*w+4*g,2*(h+lh)+3*g),'#eee9dd');d=ImageDraw.Draw(sheet);font=ImageFont.truetype(str(root/'fonts/CCUltimatum-Bold.ttf'),25)
labels=['00. Исходный', '01. Двуручная пила', '02. Пилорама', '03. Трелёвочник', '04. Леспромхоз', '05. Узкоколейка']
for i,(slug,label) in enumerate(zip(variants,labels)):
 x=g+i%3*(w+g);y=g+i//3*(h+lh+g);d.text((x+w/2,y+5),label,font=font,fill='#123E70',anchor='mt');im=Image.open(root/f'cards/{slug}.png').convert('RGB');sheet.paste(im.resize((w,h),Image.Resampling.LANCZOS),(x,y+lh))
sheet.save(root/'cards/lesopoval-six-approved.jpg',quality=95)
