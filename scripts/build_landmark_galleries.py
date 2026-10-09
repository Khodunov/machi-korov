#!/usr/bin/env python3
"""Collect the latest five variants of each landmark with their paired backs."""
from pathlib import Path
from PIL import Image, ImageOps
import re,json
root=Path(__file__).resolve().parents[1]
out=root/'cards/landmarks-five-player';out.mkdir(exist_ok=True)
groups=[('kreml','Кремль'),('zhd-stantsiya','ЖД станция'),('torgovyy-tsentr','Торговый центр'),('mfc','МФЦ'),('gostelekanal','Гостелеканал'),('tec','ТЭЦ'),('airport','Аэропорт')]
manifest=[]
for prefix,title in groups:
    slugs=[]
    for i in range(1,6):
        candidates=list((root/'cards').glob(f'{prefix}-{i:02d}-*.png'))
        candidates=[p for p in candidates if not any(x in p.stem for x in ['preview','back','front'])]
        def version(p):
            m=re.search(r'-v(\d+)$',p.stem)
            return int(m.group(1)) if m else 1
        p=max(candidates,key=version)
        assert prefix=='kreml' or (root/'card-backs'/p.name).exists(),p
        slugs.append(p.stem)
    folders=['cards','card-backs']
    backs=['card-backs/starter-v1.png' if prefix=='kreml' else f'card-backs/{slug}.png'
           for slug in slugs]
    sheet=Image.new('RGB',(5*410+6*16,len(folders)*615+(len(folders)+1)*16),'#f4f0e8')
    for row,folder in enumerate(folders):
        for col,slug in enumerate(slugs):
            source=root/backs[col] if row==1 else root/folder/(slug+'.png')
            im=Image.open(source).convert('RGBA')
            im=ImageOps.contain(im,(410,615),Image.Resampling.LANCZOS)
            sheet.paste(im,(16+col*426+(410-im.width)//2,16+row*631+(615-im.height)//2),im)
    sheet.save(out/(prefix+'.jpg'),quality=93)
    manifest.append(dict(title=title,copies=5,variants=slugs,backs=backs))
(out/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2))
overview=Image.new('RGB',(2048,1536),'#FBF8F0')
for index,item in enumerate(manifest):
    card=Image.open(root/'cards'/(item['variants'][0]+'.png')).convert('RGB')
    overview.paste(card.resize((512,768),Image.Resampling.LANCZOS),
                   ((index%4)*512,(index//4)*768))
overview.save(out/'overview.jpg',quality=94)
print(f'Saved 7 galleries (35 cards), overview and manifest to {out}')
