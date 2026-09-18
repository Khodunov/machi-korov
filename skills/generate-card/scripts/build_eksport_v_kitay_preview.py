from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
root=Path(__file__).resolve().parents[3]
variants=['eksport-v-kitay', 'eksport-v-kitay-01-pogruzchik-v2', 'eksport-v-kitay-02-konteynerovoz-v2', 'eksport-v-kitay-03-tanker-v2', 'eksport-v-kitay-04-gruzoviki-v2', 'eksport-v-kitay-05-sostavy-v2']
w,h,g,lh=550,715,18,42
sheet=Image.new('RGB',(3*w+4*g,2*(h+lh)+3*g),'#eee9dd');d=ImageDraw.Draw(sheet);font=ImageFont.truetype(str(root/'fonts/CCUltimatum-Bold.ttf'),25)
labels=['00. Исходный', '01. Погрузчик', '02. Контейнеровоз', '03. Танкер', '04. Грузовики', '05. Составы']
for i,(slug,label) in enumerate(zip(variants,labels)):
 x=g+i%3*(w+g);y=g+i//3*(h+lh+g);d.text((x+w/2,y+5),label,font=font,fill='#17361A',anchor='mt');im=Image.open(root/f'cards/{slug}.png').convert('RGB');sheet.paste(im.resize((w,h),Image.Resampling.LANCZOS),(x,y+lh))
sheet.save(root/'cards/eksport-v-kitay-six-approved.jpg',quality=95)
