#!/usr/bin/env python3
"""Extract the original vector paths, without tracing or image generation.

Requires PyMuPDF. Source: IDW rulebook, PDF page 7, first unbuilt landmark.
Run from repository root. Outputs standalone SVG and transparent PNG.
"""
from pathlib import Path
import hashlib
import json
import pymupdf as fitz

source = Path('references/machi-koro-original-rules-idw.pdf')
doc = fitz.open(source)
paths = doc[6].get_drawings()[3391:3407]
assert len(paths) == 16 and abs(paths[0]['rect'].x0 - 120.93) < .01
assert all(paths[0]['rect'].contains(p['rect']) for p in paths)
def export(paths, stem, padding):
    # Preserve the original curves, colors, stroke weights and stacking order.
    out = fitz.open()
    page = out.new_page(width=493.227997, height=637.794983)
    for path in paths:
        shape = page.new_shape()
        for item in path['items']:
            if item[0] == 'l':
                shape.draw_line(item[1], item[2])
            elif item[0] == 'c':
                shape.draw_bezier(*item[1:])
            else:
                raise ValueError(f'Unexpected source primitive: {item[0]}')
        shape.finish(fill=path['fill'], color=path['color'],
                     width=path['width'] or 0,
                     closePath=path['type'] == 'f' or bool(path['closePath']),
                     even_odd=bool(path['even_odd']),
                     lineCap=max(path['lineCap'] or (0,)),
                     lineJoin=path['lineJoin'] or 0)
        shape.commit()
    box = paths[0]['rect'] + (-padding, -padding, padding, padding)
    page.set_cropbox(box)
    Path(f'icons/{stem}.svg').write_text(page.get_svg_image())
    page.get_pixmap(matrix=fitz.Matrix(1024/page.rect.width, 1024/page.rect.width),
                   alpha=True).save(f'icons/{stem}.png')

export(paths, "landmark-construction-original", .2)
export(doc[6].get_drawings()[17786:17788], "landmark", .4)
Path('references/landmark-construction-source.json').write_text(json.dumps({
    'source_url': 'https://cdn.1j1ju.com/medias/89/cb/e8-machi-koro-rulebook.pdf',
    'source_file': str(source), 'sha256': hashlib.sha256(source.read_bytes()).hexdigest(),
    'pdf_page_one_based': 7, 'drawing_indices': [3391, 3406],
    'title_badge_drawing_indices': [17786, 17787],
    'method': 'Extract original vector curves and fills; no tracing or generative redraw.',
    'outputs': ['icons/landmark-construction-original.svg', 'icons/landmark-construction-original.png',
                'icons/landmark.svg', 'icons/landmark.png']
}, indent=2) + '\n')
