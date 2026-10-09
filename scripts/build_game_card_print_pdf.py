#!/usr/bin/env python3
"""60 x 90 mm establishment cards with 3 mm corners, A4 long-edge duplex."""
import json
import math
from pathlib import Path

from PIL import Image
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfgen.canvas import Canvas
from pypdf import PdfReader, PdfWriter
from pypdf.generic import DictionaryObject, NameObject
from pdf_print_utils import compact_image_streams

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / 'output/pdf/game-cards-139-duplex-a4-60x90-rounded.pdf'
QA = ROOT / 'tmp/pdfs/game-cards'
PAGE_W, PAGE_H = A4
W, H, GAP = 60 * mm, 90 * mm, 4 * mm
CORNER_RADIUS = 3 * mm
LEFT = (PAGE_W - 3 * W - 2 * GAP) / 2
BOTTOM = (PAGE_H - 3 * H - 2 * GAP) / 2
# Inside the actual colored edges, excluding antialiasing and export shadows.
BOUNDS = {
    'blue': (79, 32, 945, 1497),
    'green': (80, 32, 944, 1497),
    'red': (81, 32, 943, 1497),
    'purple': (64, 35, 961, 1486),
    'back': (27, 23, 998, 1511),
}


def prepare_image(source, category):
    image = Image.open(ROOT / source).convert('RGB').crop(BOUNDS[category])
    # Extend the existing edge texture into rounded export corners, so faces
    # and backs have the same opaque rectangular trim boundary with no cream.
    radius = 90
    for y in range(radius):
        inset = math.ceil(radius - math.sqrt(radius**2 - (radius-y)**2)) + 3
        for yy in (y, image.height-1-y):
            for start, stop, sample in ((0, inset, inset),
                                        (image.width-inset, image.width, image.width-inset-1)):
                image.paste(image.getpixel((sample, yy)), (start, yy, stop, yy+1))
    path = QA / 'artwork' / (Path(source).stem + '.jpg')
    image.save(path, quality=98, subsampling=0)
    return path


def position(row, col):
    return LEFT + col*(W+GAP), BOTTOM + (2-row)*(H+GAP)


def crop_marks(pdf, x, y):
    pdf.setStrokeColorRGB(.45, .45, .45)
    pdf.setLineWidth(.25)
    offset, length = .5*mm, 1.3*mm
    for xx in (x, x+W):
        pdf.line(xx, y-offset, xx, y-offset-length)
        pdf.line(xx, y+H+offset, xx, y+H+offset+length)
    for yy in (y, y+H):
        pdf.line(x-offset, yy, x-offset-length, yy)
        pdf.line(x+W+offset, yy, x+W+offset+length, yy)


def main():
    (QA / 'artwork').mkdir(parents=True, exist_ok=True)
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    groups = json.loads((ROOT / 'cards/game-cards-with-backs/manifest.json').read_text())
    config = {c['slug']: c for c in json.loads((ROOT / 'cards-config.json').read_text())['cards']}
    cards, prepared = [], {}
    for group in groups:
        assert group['copies'] == len(group['cards'])
        for copy in group['cards']:
            card = dict(copy, id=len(cards)+1)
            cards.append(card)
            for side in ('front', 'back'):
                source = card[side]
                category = config[group['slug']]['category'] if side == 'front' else 'back'
                if source not in prepared:
                    prepared[source] = prepare_image(source, category)
    assert len(cards) == 139
    sheets = math.ceil(len(cards)/9)
    pdf = Canvas(str(OUTPUT), pagesize=A4, pageCompression=1)
    pdf.setTitle('Machi Korov - 139 cards - 60 x 90 mm - A4 duplex')
    pdf.setAuthor('Machi Korov')
    pdf.setSubject('Actual size 100%; A4 portrait; duplex flip on long edge')
    placements = []
    for sheet in range(sheets):
        for side in ('front', 'back'):
            page = 2*sheet + (1 if side == 'front' else 2)
            pdf.setFont('Helvetica', 7)
            pdf.setFillColorRGB(.25, .25, .25)
            pdf.drawCentredString(PAGE_W/2, PAGE_H-5*mm,
                                  f'Machi Korov | Sheet {sheet+1}/{sheets} | {side.upper()} | Page {page}/{2*sheets}')
            for index, card in enumerate(cards[sheet*9:(sheet+1)*9]):
                row, col = divmod(index, 3)
                if side == 'back':
                    col = 2-col
                x, y = position(row, col)
                pdf.saveState()
                path = pdf.beginPath()
                path.roundRect(x, y, W, H, CORNER_RADIUS)
                pdf.clipPath(path, stroke=0, fill=0)
                pdf.drawImage(str(prepared[card[side]]), x, y, width=W, height=H)
                pdf.restoreState()
                if side == 'front':
                    crop_marks(pdf, x, y)
                pdf.setFont('Helvetica', 5)
                pdf.drawCentredString(x+W/2, y-2.2*mm, str(card['id']))
                placements.append(dict(page=page, side=side, card=card['id'],
                                       source=card[side], x=x, y=y, w=W, h=H))
            pdf.setFont('Helvetica', 6.5)
            pdf.drawCentredString(PAGE_W/2, 4.5*mm,
                                  'A4 | 60 x 90 mm | Actual size 100% | Duplex: flip on LONG edge')
            pdf.showPage()
    pdf.save()
    writer = PdfWriter()
    writer.clone_document_from_reader(PdfReader(OUTPUT))
    writer._root_object[NameObject('/ViewerPreferences')] = DictionaryObject({
        NameObject('/Duplex'): NameObject('/DuplexFlipLongEdge'),
        NameObject('/PrintScaling'): NameObject('/None'),
    })
    compact_image_streams(writer)
    with OUTPUT.open('wb') as stream:
        writer.write(stream)
    for card in cards:
        front, back = [p for p in placements if p['card'] == card['id']]
        assert back['page'] == front['page']+1
        assert abs(front['x']+back['x']+W-PAGE_W) < 1e-8
        assert front['y'] == back['y'] and front['w'] == back['w'] and front['h'] == back['h']
    assert len(PdfReader(OUTPUT).pages) == 32
    (QA / 'imposition.json').write_text(json.dumps(placements, indent=2))
    print(f'{OUTPUT}: 32 pages, 16 sheets, 139 matching pairs; {OUTPUT.stat().st_size/1024/1024:.1f} MiB')


if __name__ == '__main__':
    main()
