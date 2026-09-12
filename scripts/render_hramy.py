"""Rebuild church cutouts and cards from preserved image_gen sources."""
from pathlib import Path
import subprocess,sys,json
import numpy as np
from PIL import Image
ROOT=Path(__file__).resolve().parents[1]
SLUGS=['hram-01-maybach','hram-02-vsem-mirom','hram-03-svechi-kartoy','hram-04-blagodetel']
def main():
 import os
 os.chdir(ROOT)
 # Looser neutral-background threshold below the scene removes generated floor shadows.
 source=Path('skills/generate-card/scripts/remove_light_background.py').read_text()
 source=source.replace('candidate = ((low >= 235) & ((high - low) <= 22)).astype(np.uint8)', 'lower = np.indices(low.shape)[0] > low.shape[0] * 0.75\n    candidate = (((low >= 235) & ((high - low) <= 22)) | (lower & (low >= 195) & ((high - low) <= 30))).astype(np.uint8)')
 ns={'__name__':'hramy_background'}
 exec(compile(source,'hramy_background','exec'),ns)
 for slug in SLUGS[1:]:
  seeds=[(220,475)] if slug==SLUGS[1] else []
  ns['remove_background'](Path(f'buildings/{slug}-source.png'),Path(f'buildings/{slug}.png'),seeds)
 for slug in SLUGS:
  subprocess.run(['bash','-n',f'card-commands/{slug}.sh'],check=True)
  subprocess.run(['bash',f'card-commands/{slug}.sh'],check=True)
 out=Image.new('RGB',(1100,1430),'#eee9e0')
 for i,slug in enumerate(SLUGS):
  im=Image.open(f'cards/{slug}.png').convert('RGB'); im.thumbnail((550,715)); out.paste(im,((i%2)*550,(i//2)*715))
 out.save('cards/hramy-four-cards.jpg',quality=95)
if __name__=='__main__': main()
