#!/usr/bin/env python3
"""Rebuild beer-kiosk cutouts, cards and contact sheets from saved sources."""
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter

ROOT = Path(__file__).resolve().parents[1]
LABELS = ['А вот ту жвачку!', 'По одной — и домой', 'Под козырьком', 'Тропа народная', 'Большой футбол', 'Островок торговли', 'Без сдачи', 'На минутку', 'Рыбный инспектор', 'Последний покупатель']

def main():
    os.chdir(ROOT)
    records = json.loads(Path('prompts/central-illustrations/pivnye-larki-v3-generation-records.json').read_text())
    manifest = []
    base_command = Path('card-commands/pivnoy-laryok.sh').read_text().replace('  --flip-horizontal \\\n', '')
    for i, record in enumerate(records):
        slug = 'pivnoy-laryok-' + record['id'] + '-v3'
        source = Path('buildings') / (slug + '-source.png')
        hint = record.get('edit_output_hint') or record.get('output_hint')
        if hint and not source.exists():
            path = re.search(r' as (/.+?\.png) by default', hint).group(1)
            shutil.copy2(path, source)
        if not source.exists():
            continue
        cutout = Path('buildings') / (slug + '.png')
        processing_source = source
        if record.get('label_cleanup'):
            clean = Image.open(source).convert('RGB')
            for patch in record['label_cleanup']:
                mask = Image.new('L', (clean.width * 4, clean.height * 4), 0)
                ImageDraw.Draw(mask).polygon([(x * 4, y * 4) for x, y in patch['polygon']], fill=255)
                mask = mask.resize(clean.size, Image.Resampling.LANCZOS)
                clean.paste(Image.new('RGB', clean.size, patch['color']), (0, 0), mask)
            processing_source = Path('buildings') / (slug + '-cleaned-source.png')
            clean.save(processing_source)
        if record.get('wall_cleanup'):
            cleanup = record['wall_cleanup']
            clean = Image.open(source).convert('RGB')
            polygon = [tuple(p) for p in cleanup['target_polygon']]
            x0, y0 = min(p[0] for p in polygon), min(p[1] for p in polygon)
            x1, y1 = max(p[0] for p in polygon), max(p[1] for p in polygon)
            sample = clean.crop(cleanup['source_box'])
            sample = sample.resize((x1-x0, sample.height), Image.Resampling.BICUBIC)
            texture = Image.new('RGB', (x1-x0, y1-y0))
            for n, y in enumerate(range(0, texture.height, sample.height)):
                texture.paste(sample if n % 2 == 0 else sample.transpose(Image.Transpose.FLIP_TOP_BOTTOM), (0, y))
            layer = clean.copy()
            layer.paste(texture, (x0, y0))
            mask = Image.new('L', clean.size, 0)
            ImageDraw.Draw(mask).polygon(polygon, fill=255)
            mask = mask.filter(ImageFilter.GaussianBlur(1.2))
            processing_source = Path('tmp/imagegen/pivnye-larki-v3') / (slug + '-wall-cleaned.png')
            processing_source.parent.mkdir(parents=True, exist_ok=True)
            Image.composite(layer, clean, mask).save(processing_source)
        if record.get('crop_box'):
            processing_source = Path('tmp/imagegen/pivnoy-laryok') / (slug + '-selected-view.png')
            processing_source.parent.mkdir(parents=True, exist_ok=True)
            Image.open(source).crop(record['crop_box']).save(processing_source)
        if not cutout.exists() or source.stat().st_mtime > cutout.stat().st_mtime or record.get('background_seeds') or record.get('background_regions') or record.get('crop_box') or record.get('wall_cleanup') or record.get('label_cleanup'):
            remove_command = [sys.executable, 'skills/generate-card/scripts/remove_light_background.py', str(processing_source), str(cutout)]
            for x, y in record.get('background_seeds', []):
                remove_command += ['--background-seed', str(x), str(y)]
            for region in record.get('background_regions', []):
                remove_command += ['--background-region', *map(str, region)]
            subprocess.run(remove_command, check=True)
        bounds = Image.open(cutout).getchannel('A').getbbox()
        aspect = (bounds[3] - bounds[1]) / (bounds[2] - bounds[0])
        scale = min(0.78, 0.42 * 1430 / (1100 * aspect))
        height = 1100 * scale * aspect
        y_frac = 0.735 - height / (2 * 1430)
        command = base_command.replace('buildings/pivnoy-laryok.png', str(cutout)).replace('cards/pivnoy-laryok.png', f'cards/{slug}.png')
        command = command.replace('--scale 0.62', f'--scale {scale:.4f}').replace('--y-frac 0.52', f'--y-frac {y_frac:.4f}')
        command_path = Path('card-commands') / (slug + '.sh')
        command_path.write_text(command)
        subprocess.run(['bash', '-n', str(command_path)], check=True)
        subprocess.run(['bash', str(command_path)], check=True, stdout=subprocess.DEVNULL)
        spec = {'use_case': 'illustration-story', 'title': LABELS[i], 'tool': 'built-in image_gen', 'prompt': record.get('prompt'), 'edit_prompt': record.get('edit_prompt'), 'source': str(source), 'cutout': str(cutout), 'card': f'cards/{slug}.png', 'background': 'Plain white generated source; local edge-connected background removal.', 'references': record.get('references', []), 'orientation': 'Use generated orientation without mirroring.'}
        spec['visual_style_references'] = record.get('visual_style_references', [])
        spec['local_processing'] = {key: record[key] for key in ['wall_cleanup', 'background_regions', 'background_seeds', 'label_cleanup'] if key in record}
        Path(f'prompts/central-illustrations/{slug}.json').write_text(json.dumps(spec, ensure_ascii=False, indent=2) + '\n')
        manifest.append(spec)
    Path('prompts/central-illustrations/pivnye-larki-v3-production.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n')
    for mode, tile in [('art', (440, 460)), ('cards', (440, 604))]:
        tw, th = tile
        gap = 18
        sheet = Image.new('RGB', (tw * 5 + gap * 6, th * 2 + gap * 3), '#e9edf2')
        draw = ImageDraw.Draw(sheet)
        font = ImageFont.truetype('fonts/Boingster-Regular.ttf', 18)
        for i, record in enumerate(records):
            slug = 'pivnoy-laryok-' + record['id'] + '-v3'
            path = Path(f'buildings/{slug}.png' if mode == 'art' else f'cards/{slug}.png')
            if not path.exists():
                continue
            im = Image.open(path).convert('RGBA')
            if mode == 'art':
                im = im.crop(im.getchannel('A').getbbox())
            im.thumbnail((tw, th - 38), Image.Resampling.LANCZOS)
            x = gap + (i % 5) * (tw + gap)
            y = gap + (i // 5) * (th + gap)
            sheet.paste(im, (x + (tw - im.width)//2, y + (th - 38 - im.height)//2), im)
            draw.text((x + tw//2, y + th - 26), f'{i+1}. {LABELS[i]}', font=font, fill='#17361A', anchor='mt')
        collection = 'ten' if len(manifest) == 10 else 'partial'
        sheet.save(f'cards/pivnye-larki-v3-{collection}-{mode}.jpg', quality=95)
    print(f'Rendered {len(manifest)} variants.')

if __name__ == '__main__':
    main()
