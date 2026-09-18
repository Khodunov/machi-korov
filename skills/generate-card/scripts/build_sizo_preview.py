from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
root=Path(__file__).resolve().parents[3]
variants=['sizo', 'sizo-01-avtozak', 'sizo-02-peredachi', 'sizo-03-kresty', 'sizo-04-matrosskaya-tishina']
w,h,g,lh=550,715,18,42
sheet=Image.new('RGB',(3*w+4*g,2*(h+lh)+3*g),'#eee9dd');d=ImageDraw.Draw(sheet);font=ImageFont.truetype(str(root/'fonts/CCUltimatum-Bold.ttf'),25)
labels=['00. Исходное', '01. Автозак', '02. Передачи', '03. Кресты', '04. Матросская Тишина']
for i,(slug,label) in enumerate(zip(variants,labels)):
 x=g+i%3*(w+g);y=g+i//3*(h+lh+g);d.text((x+w/2,y+5),label,font=font,fill='#3E1F59',anchor='mt');im=Image.open(root/f'cards/{slug}.png').convert('RGB');sheet.paste(im.resize((w,h),Image.Resampling.LANCZOS),(x,y+lh))
sheet.save(root/'cards/sizo-five-approved.jpg',quality=95)
