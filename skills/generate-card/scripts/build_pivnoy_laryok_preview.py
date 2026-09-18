from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
root=Path(__file__).resolve().parents[3]
variants=['pivnoy-laryok', 'pivnoy-laryok-01-zhvachka-v3', 'pivnoy-laryok-02-domoy-v3', 'pivnoy-laryok-03-kozyrek-v3', 'pivnoy-laryok-04-tropa-v3', 'pivnoy-laryok-05-futbol-v3', 'pivnoy-laryok-06-ostrovok-v3', 'pivnoy-laryok-07-bez-sdachi-v3', 'pivnoy-laryok-08-minutka-v3', 'pivnoy-laryok-09-kot-v3', 'pivnoy-laryok-10-novyy-god-v3']
w,h,g,lh=440,572,16,38
sheet=Image.new('RGB',(4*w+5*g,3*(h+lh)+4*g),'#eee9dd');d=ImageDraw.Draw(sheet);font=ImageFont.truetype(str(root/'fonts/CCUltimatum-Bold.ttf'),23)
labels=['00. Исходный', '01. Жвачка', '02. Домой', '03. Под козырьком', '04. Тропа', '05. Футбол', '06. Островок', '07. Без сдачи', '08. На минутку', '09. Кот', '10. Новый год']
for i,(slug,label) in enumerate(zip(variants,labels)):
 x=g+i%4*(w+g);y=g+i//4*(h+lh+g);d.text((x+w/2,y+5),label,font=font,fill='#17361A',anchor='mt');im=Image.open(root/f'cards/{slug}.png').convert('RGB');sheet.paste(im.resize((w,h),Image.Resampling.LANCZOS),(x,y+lh))
sheet.save(root/'cards/pivnoy-laryok-eleven-approved.jpg',quality=95)
