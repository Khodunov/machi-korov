from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
root=Path(__file__).resolve().parents[3]
variants=['panelka', 'panelka-01-kover-v2', 'panelka-02-lebedi-v2', 'panelka-03-ogorod-v2', 'panelka-04-uteplenie-v2', 'panelka-05-kosmodrom-v2', 'panelka-06-balkony-v2', 'panelka-07-korabl-v2', 'panelka-08-sugrob-v2', 'panelka-09-mozaika-v2', 'panelka-10-tropinka-v4']
w,h,g,lh=440,572,16,38
sheet=Image.new('RGB',(4*w+5*g,3*(h+lh)+4*g),'#eee9dd');d=ImageDraw.Draw(sheet);font=ImageFont.truetype(str(root/'fonts/CCUltimatum-Bold.ttf'),23)
labels=['00. Исходная','01. Ковёр','02. Лебеди','03. Огород','04. Утепление','05. Космодром','06. Балконы','07. Корабль','08. Сугроб','09. Мозаика','10. Тропинка']
for i,(slug,label) in enumerate(zip(variants,labels)):
 x=g+i%4*(w+g);y=g+i//4*(h+lh+g);d.text((x+w/2,y+5),label,font=font,fill='#123E70',anchor='mt');im=Image.open(root/f'cards/{slug}.png').convert('RGB');sheet.paste(im.resize((w,h),Image.Resampling.LANCZOS),(x,y+lh))
sheet.save(root/'cards/panelka-eleven-approved.jpg',quality=95)
