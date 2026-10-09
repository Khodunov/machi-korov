#!/usr/bin/env python3
"""Render both landmark states from one illustration and one specification."""
from __future__ import annotations

import argparse
import math
import re
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageOps

ROOT = Path(__file__).resolve().parents[3]
SIZE = (1024, 1536)
TITLE_FONT = ROOT / "fonts/Boingster-Regular.ttf"
RULES_FONT = ROOT / "fonts/CCUltimatum-Bold.ttf"
TITLE_ICON = ROOT / "icons/landmark.png"
CONSTRUCTION_ICON = ROOT / "icons/landmark-construction-original.png"
RULES_ICONS = {
    "{shop}": ROOT / "icons/shop-stall.png",
    "{restaurant}": ROOT / "icons/glass-and-fork.png",
}
RULES_BOX = (118, 1165, 906, 1480)
COST_BOX = (111, 1325, 245, 1459)


def rules_line_left(y, height, show_cost):
    """Left boundary beside the circular coin, including a 14 px gutter."""
    left = RULES_BOX[0]
    if show_cost:
        cx = (COST_BOX[0] + COST_BOX[2]) / 2
        cy = (COST_BOX[1] + COST_BOX[3]) / 2
        radius = (COST_BOX[2] - COST_BOX[0]) / 2 + 14
        distance = max(y - cy, cy - (y + height), 0)
        if distance < radius:
            left = max(left, math.ceil(cx + math.sqrt(radius**2 - distance**2)))
    return left


def rules_text(canvas, value, show_cost=True):
    """Center vertically; let only rows beside the coin follow its contour."""
    lines = value.replace("\\n", "\n").splitlines()
    for token in re.findall(r"\{[^{}]+\}", value):
        if token not in RULES_ICONS:
            raise ValueError(f"Unknown rules icon: {token}")
    assets = {token: load_trimmed(path) for token, path in RULES_ICONS.items()
              if token in value}
    for size in range(49, 33, -1):
        font = ImageFont.truetype(str(RULES_FONT), size)
        rendered = []
        for line in lines:
            runs = re.split(r"(\{[^{}]+\})", line)
            parts = []
            for run in filter(None, runs):
                if run in assets:
                    side = round(size * 1.35)
                    part = assets[run].resize((side, side), Image.Resampling.LANCZOS)
                else:
                    b = font.getbbox(run)
                    width = max(round(font.getlength(run)), b[2]) - min(0, b[0])
                    part = Image.new("RGBA", (max(1, width), max(1, b[3]-b[1])))
                    ImageDraw.Draw(part).text((-min(0, b[0]), -b[1]), run,
                                              font=font, fill="#FFF9E9")
                parts.append(part)
            width = sum(part.width for part in parts)
            height = max((part.height for part in parts), default=size)
            row = Image.new("RGBA", (max(1, width), height))
            x = 0
            for part in parts:
                row.alpha_composite(part, (x, (height-part.height)//2))
                x += part.width
            # Center visible ink, rather than font advance and side bearings.
            bounds = row.getchannel("A").getbbox()
            rendered.append(row.crop(bounds) if bounds else row)
        height = sum(row.height for row in rendered) + 10 * (len(rendered)-1)
        if max(row.width for row in rendered) <= RULES_BOX[2]-RULES_BOX[0] and height <= RULES_BOX[3]-RULES_BOX[1]:
            y = round((RULES_BOX[1]+RULES_BOX[3]-height)/2)
            positions = []
            for row in rendered:
                x = max((SIZE[0]-row.width)//2,
                        rules_line_left(y, row.height, show_cost))
                positions.append((x, y))
                y += row.height + 10
            if any(
                x+row.width > RULES_BOX[2]
                for row, (x, y) in zip(rendered, positions)
            ):
                continue
            for row, pos in zip(rendered, positions):
                canvas.alpha_composite(row, pos)
            return
    raise ValueError(f"Centered rules do not fit clear of the coin; adjust line breaks: {value!r}")


def text(canvas, value, box, font_path, size, fill, minimum=26):
    """Fit explicit line breaks into a bounded region, failing on unreadable text."""
    value = value.replace("\\n", "\n")
    draw = ImageDraw.Draw(canvas)
    for px in range(size, minimum - 1, -1):
        font = ImageFont.truetype(str(font_path), px)
        bounds = draw.multiline_textbbox((0, 0), value, font=font, spacing=10, align="center")
        w, h = bounds[2] - bounds[0], bounds[3] - bounds[1]
        if w <= box[2] - box[0] and h <= box[3] - box[1]:
            draw.multiline_text(((box[0] + box[2] - w) / 2 - bounds[0],
                                 (box[1] + box[3] - h) / 2 - bounds[1]),
                                value, font=font, fill=fill, spacing=10, align="center")
            return
    raise ValueError(f"Text does not fit; shorten it or add line breaks: {value!r}")


def template(built, show_cost=True):
    """Code-native card furniture: no dice or activation-number region."""
    canvas = Image.new("RGBA", SIZE, "#FBF8F0")
    layer = Image.new("RGBA", SIZE)
    d = ImageDraw.Draw(layer)
    sky, pale, footer, skyline = (("#E9CB6C", "#F8E8AA", "#996335", "#C59B55") if built
                                  else ("#CBD0C4", "#E4E7DC", "#68736A", "#A5AFA2"))
    d.rectangle((76, 30, 948, 1500), fill=sky)
    # Quiet clouds leave a generous central art area.
    for x, y, scale in [(116, 375, 1), (774, 320, .7), (790, 925, .65)]:
        d.ellipse((x, y, x + 75*scale, y + 65*scale), fill="#FFF9E9")
        d.ellipse((x + 40*scale, y - 32*scale, x + 125*scale, y + 65*scale), fill="#FFF9E9")
        d.rounded_rectangle((x - 15*scale, y + 30*scale, x + 155*scale, y + 70*scale), 14, fill="#FFF9E9")
    # Deterministic skyline, with no generated text or raster template dependencies.
    for i, x in enumerate(range(76, 948, 49)):
        h = (64, 98, 50, 125, 77, 106, 58)[i % 7]
        d.rectangle((x, 1130 - h, x + 41, 1165), fill=skyline)
        for yy in range(1145 - h, 1120, 25):
            for xx in (x + 9, x + 26):
                d.rectangle((xx, yy, xx + 6, yy + 9), fill=pale)
    d.rectangle((76, 1145, 948, 1500), fill=footer)
    # Cost remains gold in both states, like a purchase affordance.
    if show_cost:
        d.ellipse(COST_BOX, fill="#F4CC4E", outline="#594832", width=5)
        d.ellipse((124, 1338, 232, 1446), outline="#594832", width=3)
    mask = Image.new("L", SIZE)
    ImageDraw.Draw(mask).rounded_rectangle((76, 30, 948, 1500), radius=48, fill=255)
    canvas.paste(layer, (0, 0), mask)
    return canvas


def load_trimmed(path):
    image = Image.open(path).convert("RGBA")
    bbox = image.getchannel("A").getbbox()
    if bbox is None:
        raise ValueError(f"Fully transparent asset: {path}")
    return image.crop(bbox)


def construction_layer(icon_path=CONSTRUCTION_ICON, width_frac=.46):
    """Independent full-card RGBA overlay shared by every unbuilt landmark."""
    layer = Image.new("RGBA", SIZE)
    icon = load_trimmed(icon_path)
    width = round(SIZE[0] * width_frac)
    height = round(width * icon.height / icon.width)
    icon = icon.resize((width, height), Image.Resampling.LANCZOS)
    layer.alpha_composite(icon, ((SIZE[0] - width)//2, 685 - height//2))
    return layer


def title_group(canvas, title, built, icon_path=TITLE_ICON):
    icon = load_trimmed(icon_path)
    if not built:
        alpha = icon.getchannel("A")
        icon = ImageOps.colorize(ImageOps.grayscale(icon), "#46554A", "#FFFFFF").convert("RGBA")
        icon.putalpha(alpha)
    draw = ImageDraw.Draw(canvas)
    value = title.replace("\\n", "\n")
    for size in range(80, 41, -1):
        font = ImageFont.truetype(str(TITLE_FONT), size)
        b = draw.multiline_textbbox((0, 0), value, font=font, spacing=10, align="center")
        w, h = b[2]-b[0], b[3]-b[1]
        badge_size, gap = round(size * 1.35), 14
        group_width = badge_size + gap + w
        if group_width <= 788 and max(h, badge_size) <= 155:
            x = (SIZE[0] - group_width) / 2
            canvas.alpha_composite(icon.resize((badge_size, badge_size), Image.Resampling.LANCZOS),
                                   (round(x), round(150.5 - badge_size / 2)))
            draw.multiline_text((x + badge_size + gap - b[0], 150.5 - h/2 - b[1]),
                                value, font=font, spacing=10, align="center",
                                fill="#624324" if built else "#46554A")
            return
    raise ValueError("Title and landmark icon do not fit; add a line break or shorten the title")


def render(art, title, rules, cost, built, title_icon=TITLE_ICON,
           construction_icon=CONSTRUCTION_ICON, construction_width_frac=.46):
    canvas = template(built, show_cost=cost is not None)
    if not built:
        alpha = art.getchannel("A")
        art = ImageOps.colorize(ImageOps.grayscale(art), "#5B675E", "#E5E8DE").convert("RGBA")
        art.putalpha(alpha)
    # Same bounding box, scale and placement on both sides, including tall landmarks.
    fitted = ImageOps.contain(art, (710, 710), Image.Resampling.LANCZOS)
    pos = ((SIZE[0] - fitted.width) // 2, 655 - fitted.height // 2)
    shadow = Image.new("RGBA", fitted.size, (48, 48, 48, 0))
    shadow.putalpha(fitted.getchannel("A").point(lambda a: round(a * .3)))
    canvas.alpha_composite(shadow, (pos[0] + 12, pos[1] + 16))
    canvas.alpha_composite(fitted, pos)
    title_group(canvas, title, built, title_icon)
    rules_text(canvas, rules, show_cost=cost is not None)
    if cost is not None:
        text(canvas, str(cost), (131, 1350, 225, 1436), TITLE_FONT, 76, "#624324", 40)
    if not built:
        canvas.alpha_composite(construction_layer(construction_icon, construction_width_frac))
    return canvas


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--overlay", type=Path, required=True)
    p.add_argument("--title", required=True)
    p.add_argument("--rules", required=True, help="Use explicit line breaks.")
    price = p.add_mutually_exclusive_group(required=True)
    price.add_argument("--cost", type=int)
    price.add_argument("--no-cost", action="store_true", help="Omit the cost coin for starting landmarks.")
    p.add_argument("--output-front", type=Path, required=True)
    p.add_argument("--output-back", type=Path, help="Omit for always-active starting landmarks.")
    p.add_argument("--preview", type=Path)
    p.add_argument("--save-templates", type=Path, help="Optional directory for blank furniture.")
    p.add_argument("--title-icon", type=Path, default=TITLE_ICON)
    p.add_argument("--construction-icon", type=Path, default=CONSTRUCTION_ICON)
    p.add_argument("--construction-width-frac", type=float, default=.46)
    p.add_argument("--output-construction-layer", type=Path,
                   help="Export the independent transparent full-card construction overlay.")
    args = p.parse_args()
    if args.cost is not None and not 0 <= args.cost <= 99:
        p.error("--cost must be between 0 and 99")
    if not .1 <= args.construction_width_frac <= .65:
        p.error("--construction-width-frac must be between .1 and .65")
    if not args.title.strip() or not args.rules.strip():
        p.error("--title and --rules must not be empty")
    if args.preview and not args.output_back:
        p.error("--preview requires --output-back")
    outputs = [args.output_front] + ([args.output_back] if args.output_back else []) + ([args.preview] if args.preview else [])
    if args.output_construction_layer:
        outputs.append(args.output_construction_layer)
    if len({path.resolve() for path in outputs}) != len(outputs):
        p.error("Output paths must be distinct")
    art = Image.open(args.overlay).convert("RGBA")
    bbox = art.getchannel("A").getbbox()
    if bbox is None:
        p.error("Illustration is fully transparent")
    art = art.crop(bbox)
    options = dict(title_icon=args.title_icon, construction_icon=args.construction_icon,
                   construction_width_frac=args.construction_width_frac)
    front = render(art, args.title, args.rules, args.cost, True, **options)
    back = render(art, args.title, args.rules, args.cost, False, **options)
    if args.output_construction_layer:
        args.output_construction_layer.parent.mkdir(parents=True, exist_ok=True)
        construction_layer(args.construction_icon, args.construction_width_frac).save(args.output_construction_layer)
    for path, im in [(args.output_front, front), (args.output_back, back)]:
        if path is None:
            continue
        path.parent.mkdir(parents=True, exist_ok=True)
        im.save(path)
    if args.preview:
        preview = Image.new("RGB", (1408, 1120), "#F0EEE7")
        text(preview, "ПОСТРОЕНО", (20, 10, 694, 70), RULES_FONT, 30, "#624324")
        text(preview, "ОБОРОТ · СТРОИТСЯ", (714, 10, 1388, 70), RULES_FONT, 30, "#46554A")
        for x, im in [(20, front), (714, back)]:
            preview.paste(im.convert("RGB").resize((674, 1011), Image.Resampling.LANCZOS), (x, 87))
        args.preview.parent.mkdir(parents=True, exist_ok=True)
        preview.save(args.preview)
    if args.save_templates:
        args.save_templates.mkdir(parents=True, exist_ok=True)
        for state, built in [("front", True), ("back", False)]:
            template(built).save(args.save_templates / f"landmark-{state}.png")


if __name__ == "__main__":
    main()
