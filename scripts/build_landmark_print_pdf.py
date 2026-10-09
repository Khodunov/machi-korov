#!/usr/bin/env python3
"""A4 duplex imposition: 35 cards, 60 x 90 mm, long-edge flip."""
import json
from pathlib import Path

from PIL import Image
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen.canvas import Canvas
from pdf_print_utils import compact_image_streams

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / 'output/pdf/landmarks-35-duplex-a4-60x90-rounded.pdf'
PAGE_W, PAGE_H = A4
W, H, GAP = 60 * mm, 90 * mm, 4 * mm
CORNER_RADIUS = 3 * mm
LEFT = (PAGE_W - (3 * W + 2 * GAP)) / 2
BOTTOM = (PAGE_H - (3 * H + 2 * GAP)) / 2


def position(row, col):
    return LEFT + col * (W + GAP), BOTTOM + (2 - row) * (H + GAP)


def artwork_bounds(source):
    # Actual colored card edges, excluding the unequal cream export margins.
    # Step inside the antialiased edge, not onto the pale transition pixels.
    return (26, 22, 999, 1512) if source == 'card-backs/starter-v1.png' else (77, 31, 948, 1500)


def draw_card(pdf, source, x, y):
    left, top, right, bottom = artwork_bounds(source)
    sx, sy = W / (right-left), H / (bottom-top)
    pdf.saveState()
    path = pdf.beginPath()
    path.roundRect(x, y, W, H, CORNER_RADIUS)
    pdf.clipPath(path, stroke=0, fill=0)
    # Extend the card's own background into the old rounded export corners.
    # Both faces have the same 60 x 90 mm silhouette with 3 mm corners.
    if source == 'card-backs/starter-v1.png':
        with Image.open(ROOT / source) as image:
            top_color = image.convert('RGB').getpixel((512, 26))
            bottom_color = image.convert('RGB').getpixel((512, 1507))
    else:
        top_color, bottom_color = ((203,208,196),(104,115,106)) if source.startswith('card-backs/') else ((233,203,108),(153,99,53))
    pdf.setFillColorRGB(*(v/255 for v in bottom_color))
    pdf.rect(x, y, W, H/2, stroke=0, fill=1)
    pdf.setFillColorRGB(*(v/255 for v in top_color))
    pdf.rect(x, y+H/2, W, H/2, stroke=0, fill=1)
    # Exclude the source's rounded cream corners. The background above fills
    # only those corners; the illustration and text are not regenerated.
    pdf.translate(x, y)
    pdf.scale(sx, sy)
    path = pdf.beginPath()
    path.roundRect(0, 0, right-left, bottom-top, 65)
    pdf.clipPath(path, stroke=0, fill=0)
    pdf.drawImage(str(ROOT / source), -left, -(1536-bottom),
                  width=1024, height=1536)
    pdf.restoreState()


def crop_marks(pdf, x, y):
    pdf.setStrokeColorRGB(.45, .45, .45)
    pdf.setLineWidth(.25)
    offset, length = .5 * mm, 1.3 * mm
    for xx in (x, x + W):
        pdf.line(xx, y-offset, xx, y-offset-length)
        pdf.line(xx, y+H+offset, xx, y+H+offset+length)
    for yy in (y, y + H):
        pdf.line(x-offset, yy, x-offset-length, yy)
        pdf.line(x+W+offset, yy, x+W+offset+length, yy)


def main():
    groups = json.loads((ROOT / 'cards/landmarks-five-player/manifest.json').read_text())
    cards = []
    for group in groups:
        assert group['copies'] == len(group['variants']) == len(group['backs']) == 5
        for slug, back in zip(group['variants'], group['backs']):
            cards.append({'id': len(cards)+1, 'front': f'cards/{slug}.png', 'back': back})
    assert len(cards) == 35
    for card in cards:
        for side in ('front', 'back'):
            with Image.open(ROOT / card[side]) as image:
                assert image.size == (1024, 1536), card[side]

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    font = Path('/System/Library/Fonts/Supplemental/Arial.ttf')
    if not font.exists():
        font = ROOT / 'fonts/CCUltimatum-Bold.ttf'
    pdfmetrics.registerFont(TTFont('PrintLabels', str(font)))
    pdf = Canvas(str(OUTPUT), pagesize=A4, pageCompression=1)
    pdf.setTitle('Достопримечательности - 35 карт - A4 - 60 x 90 мм')
    pdf.setAuthor('Machi Korov')
    pdf.setSubject('Двусторонняя печать: 100%, переворот по длинному краю')
    placements = []
    for sheet in range(4):
        batch = cards[sheet*9:(sheet+1)*9]
        for side in ('front', 'back'):
            page = sheet*2 + (1 if side == 'front' else 2)
            label = 'ЛИЦЕВЫЕ СТОРОНЫ' if side == 'front' else 'ОБОРОТЫ'
            pdf.setFont('PrintLabels', 7)
            pdf.setFillColorRGB(.25, .25, .25)
            pdf.drawCentredString(PAGE_W/2, PAGE_H-5*mm,
                                 f'Достопримечательности | Лист {sheet+1}/4 | {label} | Страница {page}/8')
            for index, card in enumerate(batch):
                row, col = divmod(index, 3)
                if side == 'back':
                    col = 2-col
                x, y = position(row, col)
                draw_card(pdf, card[side], x, y)
                if side == 'front':
                    crop_marks(pdf, x, y)
                pdf.setFont('PrintLabels', 5)
                pdf.setFillColorRGB(.4, .4, .4)
                pdf.drawCentredString(x+W/2, y-2.2*mm, f'{card["id"]:02d}')
                placements.append(dict(page=page, side=side, card=card['id'],
                                       source=card[side], crop=artwork_bounds(card[side]),
                                       x=x, y=y, w=W, h=H))
            pdf.setFont('PrintLabels', 6.5)
            pdf.setFillColorRGB(.25, .25, .25)
            pdf.drawCentredString(PAGE_W/2, 4.5*mm,
                                 'A4 | 60 x 90 мм | Масштаб 100% | Двусторонняя печать: переворот по длинному краю')
            pdf.showPage()
    pdf.save()

    # Set explicit duplex/scaling preferences; printer settings still take precedence.
    from pypdf import PdfReader, PdfWriter
    from pypdf.generic import NameObject, DictionaryObject
    reader = PdfReader(OUTPUT)
    writer = PdfWriter()
    writer.clone_document_from_reader(reader)
    writer._root_object[NameObject('/ViewerPreferences')] = DictionaryObject({
        NameObject('/Duplex'): NameObject('/DuplexFlipLongEdge'),
        NameObject('/PrintScaling'): NameObject('/None'),
    })
    compact_image_streams(writer)
    with OUTPUT.open('wb') as stream:
        writer.write(stream)

    # Every reverse occupies the reflected front rectangle; artwork is not mirrored.
    for card in cards:
        front, back = [p for p in placements if p['card'] == card['id']]
        assert back['page'] == front['page']+1
        assert abs(front['x']+back['x']+W-PAGE_W) < 1e-8
        assert front['y'] == back['y'] and front['w'] == back['w'] and front['h'] == back['h']
    assert len(PdfReader(OUTPUT).pages) == 8
    qa = ROOT / 'tmp/pdfs'
    qa.mkdir(parents=True, exist_ok=True)
    (qa / 'landmarks-imposition.json').write_text(json.dumps(placements, indent=2))
    print(f'{OUTPUT}: 8 pages, 4 sheets, 35 matched pairs; {OUTPUT.stat().st_size/1024/1024:.1f} MiB')


if __name__ == '__main__':
    main()
