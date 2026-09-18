from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw
root=Path(__file__).resolve().parents[1]
im=Image.open(root/'icons/factory-green-source.png').convert('RGB')
a=np.asarray(im).astype(float);lo=a.min(2);hi=a.max(2)
m=Image.fromarray(((hi-lo<25)&(lo>85)&(hi<240)).astype('uint8')).copy()
w,h=im.size
for x,y in [(x,y) for x in range(w) for y in (0,h-1)]+[(x,y) for y in range(h) for x in (0,w-1)]:
 if m.getpixel((x,y))==1:ImageDraw.floodfill(m,(x,y),2)
alpha=np.where(np.array(m)==2,0,255).astype('uint8')
im=im.convert('RGBA');im.putalpha(Image.fromarray(alpha));im.save(root/'icons/factory-green.png')
