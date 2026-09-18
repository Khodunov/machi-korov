"""Replace the approved door notice, preserving the original source."""
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw,ImageFont
root=Path(__file__).resolve().parents[1]
im=Image.open(root/'buildings/upravlyayushchaya-kompaniya-v2-source.png').convert('RGB')
# Inner paper area only: corners exclude its edge, pin and red underline.
quad=[(552,760),(690,774),(682,856),(544,842)]
w,h=552,300
patch=Image.new('RGB',(w,h))
a=np.zeros((h,w,3),dtype=np.uint8)
for y in range(h):a[y,:,:]=[int(228-6*y/h),int(223-6*y/h),int(215-6*y/h)]
patch=Image.fromarray(a)
d=ImageDraw.Draw(patch);font=ImageFont.truetype(str(root/'fonts/CCUltimatum-Bold.ttf'),86)
for i,t in enumerate(['ГОРЯЧАЯ','ВОДА','ОТКЛЮЧЕНА']):
 d.text((w/2, i*96+4),t,font=font,fill=(24,28,31),anchor='mt',stroke_width=0)
# Inverse perspective mapping from destination to high-resolution paper patch.
A=[];B=[]
for (x,y),(u,v) in zip(quad,[(0,0),(w,0),(w,h),(0,h)]):
 A.extend([[x,y,1,0,0,0,-u*x,-u*y],[0,0,0,x,y,1,-v*x,-v*y]]);B.extend([u,v])
coeff=np.linalg.solve(A,B)
warped=patch.transform(im.size,Image.Transform.PERSPECTIVE,coeff,Image.Resampling.BICUBIC,fillcolor=(222,217,209))
mask=Image.new('L',im.size,0);ImageDraw.Draw(mask).polygon(quad,fill=255)
im.paste(warped,(0,0),mask)
im.save(root/'buildings/upravlyayushchaya-kompaniya-v2-notice-source.png')
