"""Rebuild church cards in the garage-cooperative illustration style."""
from pathlib import Path
import subprocess,sys,os,zipfile
from PIL import Image
ROOT=Path(__file__).resolve().parents[1]
SLUGS=['hram-01-maybach','hram-02-vsem-mirom','hram-03-svechi-kartoy','hram-04-blagodetel']
def main():
 os.chdir(ROOT)
 for base in SLUGS:
  slug=base+'-v2'; source=Path(f'buildings/{slug}-source.png')
  if not source.exists(): continue
  remove=[sys.executable,'skills/generate-card/scripts/remove_light_background.py',str(source),f'buildings/{slug}.png']
  if base=='hram-01-maybach':
   remove += ['--background-region','.15','.17','.36','.17','.36','.46','.15','.46','--background-region','.39','.385','.50','.385','.50','.46','.39','.46']
  subprocess.run(remove,check=True)
  im=Image.open(f'buildings/{slug}.png'); box=im.getchannel('A').getbbox(); aspect=(box[3]-box[1])/(box[2]-box[0])
  scale=min(.74,.40*1430/(1100*aspect))
  cmd=Path('card-commands/hram.sh').read_text().replace('buildings/hram.png',f'buildings/{slug}.png').replace('cards/hram.png',f'cards/{slug}.png').replace('--scale 0.6',f'--scale {scale:.4f}').replace('--x-frac 0.48','--x-frac 0.5')
  path=Path(f'card-commands/{slug}.sh'); path.write_text(cmd)
  subprocess.run(['bash','-n',str(path)],check=True); subprocess.run(['bash',str(path)],check=True)
 for mode in ['cards','art']:
  out=Image.new('RGB',(1400,1820 if mode=='cards' else 1050),'#eee9e0'); tw=700; th=out.height//2
  for i,base in enumerate(SLUGS):
   p=Path(f'cards/{base}-v2.png' if mode=='cards' else f'buildings/{base}-v2.png')
   if not p.exists(): continue
   im=Image.open(p).convert('RGBA')
   if mode=='art': im=im.crop(im.getchannel('A').getbbox())
   im.thumbnail((tw-20,th-20)); out.paste(im,((i%2)*tw+(tw-im.width)//2,(i//2)*th+(th-im.height)//2),im)
  out.save(f'cards/hramy-four-{mode}-v2.jpg',quality=95)
 with zipfile.ZipFile('cards/hramy-four-cards-v2.zip','w',zipfile.ZIP_DEFLATED) as z:
  for base in SLUGS:
   p=Path(f'cards/{base}-v2.png')
   if p.exists(): z.write(p,p.name)
if __name__=='__main__': main()
