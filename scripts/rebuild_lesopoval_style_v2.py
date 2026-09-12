"""Rebuild locally extracted style-matched logging illustrations and cards."""
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
for spec_path in sorted((ROOT / 'prompts/central-illustrations').glob('lesopoval-0*-v2.json')):
    spec = json.loads(spec_path.read_text())
    slug = spec_path.stem
    args = [str(ROOT / '.venv/bin/python'), 'skills/generate-card/scripts/remove_light_background.py',
            f'buildings/originals/{slug}.png', f'buildings/{slug}.png']
    for x, y in spec.get('background_seeds', []):
        args += ['--background-seed', str(x), str(y)]
    subprocess.run(args, cwd=ROOT, check=True)
    subprocess.run(['bash', '-n', f'card-commands/{slug}.sh'], cwd=ROOT, check=True)
    subprocess.run(['bash', f'card-commands/{slug}.sh'], cwd=ROOT, check=True)
