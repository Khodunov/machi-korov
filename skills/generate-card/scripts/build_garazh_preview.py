from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
root=Path(__file__).resolve().parents[3]
variants=['garazhnyy-kooperativ', 'garazhnyy-kooperativ-batina-volga', 'garazhnyy-kooperativ-kartoshka-v2', 'garazhnyy-kooperativ-rakushka-v2', 'garazhnyy-kooperativ-rybalka-v2', 'garazhnyy-kooperativ-seychas-zavedem-v2']
w,h,g,lh=550,715,18,42
sheet=Image.new('RGB',(3*w+4*g,2*(h+lh)+3*g),'#eee9dd');d=ImageDraw.Draw(sheet);font=ImageFont.truetype(str(root/'fonts/CCUltimatum-Bold.ttf'),25)
labels=['00. Исходный', '01. Батина Волга', '02. Картошка', '03. Ракушка', '04. Рыбалка', '05. Сейчас заведём']
for i,(slug,label) in enumerate(zip(variants,labels)):
 x=g+i%3*(w+g);y=g+i//3*(h+lh+g);d.text((x+w/2,y+5),label,font=font,fill='#123E70',anchor='mt');im=Image.open(root/f'cards/{slug}.png').convert('RGB');sheet.paste(im.resize((w,h),Image.Resampling.LANCZOS),(x,y+lh))
sheet.save(root/'cards/garazhnyy-kooperativ-six-approved.jpg',quality=95)
