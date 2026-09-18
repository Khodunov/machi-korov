#!/usr/bin/env python3
"""Remove baked neutral checkerboard while retaining colored refinery details."""
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

ROOT = Path(__file__).resolve().parents[1]
SLUGS = ['npz-gazprom-neft', 'npz-tatneft', 'npz-surgutneftegaz', 'npz-bashneft']

def remove(slug):
    im=Image.open(ROOT/'buildings'/f'{slug}-source.png').convert('RGB')
    rgb=np.array(im).astype(float)
    lo=rgb.min(2); hi=rgb.max(2)
    # Checkerboard is neutral gray; steel retains its blue/warm shading.
    candidate=(hi-lo<13)&(lo>100)&(hi<233)
    mask=Image.fromarray(candidate.astype('uint8'))
    w,h=im.size
    for x,y in [(x,y) for x in range(w) for y in (0,h-1)]+[(x,y) for y in range(h) for x in (0,w-1)]:
        if mask.getpixel((x,y))==1:ImageDraw.floodfill(mask,(x,y),2)
    outside=np.array(mask)==2
    # Review enclosed neutral components; checker squares have a wide luminance range.
    pending=(np.array(mask)==1)
    for yy,xx in np.argwhere(pending):
        if not pending[yy,xx]:continue
        todo=[(int(yy),int(xx))];points=[];pending[yy,xx]=False
        while todo:
            y,x=todo.pop();points.append((y,x))
            for ny,nx in ((y-1,x),(y+1,x),(y,x-1),(y,x+1)):
                if 0<=ny<h and 0<=nx<w and pending[ny,nx]:
                    pending[ny,nx]=False;todo.append((ny,nx))
        if len(points)>45:
            ys,xs=zip(*points);values=rgb[ys,xs,0]
            if np.percentile(values,90)-np.percentile(values,10)>35:outside[ys,xs]=True
    # Preserve the smoke silhouettes reviewed in each original source.
    clouds = {
      'npz-gazprom-neft': [[(57,148,15),(59,129,17),(77,108,23),(83,130,16),(104,114,20),(121,80,23),(148,54,10)],[(66,170,12),(72,153,17),(93,142,20),(100,116,23),(128,100,22),(159,74,13)]],
      'npz-tatneft': [[(77,158,15),(79,138,21),(98,112,23),(105,133,19),(127,122,20),(142,84,25),(169,57,12)],[(106,156,15),(114,131,21),(136,109,22),(143,92,25),(153,127,17),(171,78,23),(192,45,12)]],
      'npz-surgutneftegaz': [[(80,180,15),(84,162,19),(103,135,26),(109,155,19),(131,145,21),(139,118,21),(159,90,23),(182,69,11)],[(121,148,15),(133,121,23),(151,89,22),(166,111,20),(185,66,25),(196,46,17)]],
      'npz-bashneft': [[(63,140,14),(66,122,18),(86,99,23),(88,122,17),(110,107,19),(128,72,23),(153,46,10)],[(70,166,13),(78,147,18),(95,139,16),(103,115,21),(129,101,22),(116,134,17),(151,104,20),(175,67,13)]]
    }
    protect=Image.new('L',im.size,0);draw=ImageDraw.Draw(protect)
    for (ox,oy),circles in zip([(240,50),(1170,170)],clouds[slug]):
        for cx,cy,r in circles:
            draw.ellipse((ox+cx-r,oy+cy-r,ox+cx+r,oy+cy+r),fill=255)
    outside[np.array(protect)>0]=False
    alpha=Image.fromarray((~outside).astype('uint8')*255)
    rgba=im.convert('RGBA');rgba.putalpha(alpha)
    rgba.save(ROOT/'buildings'/f'{slug}.png')
    print(slug, 'transparent',round(float(outside.mean()),3))

if __name__=='__main__':
    for slug in SLUGS:remove(slug)
