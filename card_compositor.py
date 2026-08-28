#!/usr/bin/env python3
"""Composite a floating illustration onto a Machi Koro-style card template.

Supports:
- overlay placement / scale / horizontal flip
- single-digit coin number
- activation number
- centered title
- optional icon glued before the title; icon + title are centered as one group
- centered multiline bottom text
- independent font-file paths for all four text elements

Example:
    python composite_machi_koro_card.py \
      --template blue.png \
      --overlay panelka.png \
      --output result.png \
      --x-frac 0.49 \
      --y-frac 0.555 \
      --scale 0.65 \
      --flip-horizontal \
      --coin-number 1 \
      --activation-number 1 \
      --title 'Панелька' \
      --title-color '#123E70' \
      --bottom-text $'Возьмите 1 монету за ЖКХ.\nВ ход любого игрока' \
      --bottom-text-y-frac 0.905 \
      --bottom-text-font-size-frac 0.028 \
      --bottom-text-spacing-px 6
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path
from typing import Tuple

from PIL import Image, ImageDraw, ImageFont

Color = Tuple[int, int, int, int]

# These work in the OpenAI/Linux runtime. On another machine, pass the
# corresponding --*-font flags if these paths do not exist.
DEFAULT_COIN_FONT = Path("/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf")
DEFAULT_UI_FONT = Path("/usr/share/fonts/truetype/comfortaa/Comfortaa-Bold.ttf")


def trim_transparent(im: Image.Image) -> Image.Image:
    if im.mode != "RGBA":
        im = im.convert("RGBA")
    bbox = im.getchannel("A").getbbox()
    if bbox is None:
        raise ValueError("Image is fully transparent.")
    return im.crop(bbox)


def parse_hex_color(value: str) -> Color:
    value = value.strip()
    if re.fullmatch(r"#[0-9A-Fa-f]{3}", value):
        value = "#" + "".join(ch * 2 for ch in value[1:])
    if not re.fullmatch(r"#[0-9A-Fa-f]{6}", value):
        raise ValueError(f"Invalid hex color {value!r}; use #RGB or #RRGGBB.")
    return tuple(int(value[i : i + 2], 16) for i in (1, 3, 5)) + (255,)


def load_font(font_path: Path, size: int, label: str) -> ImageFont.FreeTypeFont:
    if not font_path.exists():
        raise FileNotFoundError(
            f"{label} font not found: {font_path}\n"
            f"Pass an existing font file with the corresponding --*-font flag."
        )
    return ImageFont.truetype(str(font_path), max(1, size))


def normalize_multiline_text(text: str | None) -> str | None:
    if text is None:
        return None
    # Support actual newlines, a literal backslash-n, and the accidental /n form.
    return text.replace("\\n", "\n").replace("/n", "\n")


def draw_centered_text(
    canvas: Image.Image,
    text: str,
    *,
    x_frac: float,
    y_frac: float,
    font_size_frac: float,
    font_path: Path,
    font_label: str,
    fill: Color,
    stroke_width: int = 0,
    stroke_fill: Color | None = None,
    spacing_px: int = 0,
) -> None:
    text = normalize_multiline_text(text) or ""
    draw = ImageDraw.Draw(canvas)
    font = load_font(font_path, int(round(canvas.width * font_size_frac)), font_label)

    bbox = draw.multiline_textbbox(
        (0, 0), text, font=font, spacing=spacing_px, align="center", stroke_width=stroke_width
    )
    text_w = bbox[2] - bbox[0]
    text_h = bbox[3] - bbox[1]

    cx = canvas.width * x_frac
    cy = canvas.height * y_frac
    x = cx - text_w / 2 - bbox[0]
    y = cy - text_h / 2 - bbox[1]

    draw.multiline_text(
        (x, y),
        text,
        font=font,
        fill=fill,
        spacing=spacing_px,
        align="center",
        stroke_width=stroke_width,
        stroke_fill=stroke_fill,
    )


def draw_coin_number(
    canvas: Image.Image,
    digit: str,
    *,
    x_frac: float,
    y_frac: float,
    font_size_frac: float,
    font_path: Path,
) -> None:
    if len(digit) != 1 or digit not in "0123456789":
        raise ValueError("--coin-number must be exactly one digit from 0 to 9.")
    draw_centered_text(
        canvas,
        digit,
        x_frac=x_frac,
        y_frac=y_frac,
        font_size_frac=font_size_frac,
        font_path=font_path,
        font_label="coin-number",
        fill=(103, 68, 8, 255),
        stroke_width=1,
        stroke_fill=(58, 37, 4, 255),
    )


def draw_centered_title_group(
    canvas: Image.Image,
    title: str,
    *,
    x_frac: float,
    y_frac: float,
    font_size_frac: float,
    font_path: Path,
    fill: Color,
    title_icon_path: Path | None,
    title_icon_scale: float,
    title_icon_gap_px: int,
    title_icon_y_offset_px: int,
    title_group_offset_x_px: int,
    title_group_offset_y_px: int,
) -> None:
    title = normalize_multiline_text(title) or ""
    draw = ImageDraw.Draw(canvas)
    font = load_font(font_path, int(round(canvas.width * font_size_frac)), "title")

    text_bbox = draw.multiline_textbbox((0, 0), title, font=font, align="center")
    text_w = text_bbox[2] - text_bbox[0]
    text_h = text_bbox[3] - text_bbox[1]

    icon = None
    icon_size = 0
    icon_gap = 0
    if title_icon_path is not None:
        if not title_icon_path.exists():
            raise FileNotFoundError(f"Title icon not found: {title_icon_path}")
        icon = Image.open(title_icon_path).convert("RGBA")
        icon = trim_transparent(icon)
        icon_size = max(1, int(round(text_h * title_icon_scale)))
        icon = icon.resize((icon_size, icon_size), Image.Resampling.LANCZOS)
        icon_gap = max(0, title_icon_gap_px)

    group_w = text_w + (icon_size + icon_gap if icon is not None else 0)
    group_h = max(text_h, icon_size)

    cx = canvas.width * x_frac + title_group_offset_x_px
    cy = canvas.height * y_frac + title_group_offset_y_px
    group_left = cx - group_w / 2

    if icon is not None:
        icon_x = int(round(group_left))
        icon_y = int(round(cy - icon_size / 2 + title_icon_y_offset_px))
        canvas.alpha_composite(icon, (icon_x, icon_y))
        text_x = group_left + icon_size + icon_gap - text_bbox[0]
    else:
        text_x = group_left - text_bbox[0]

    text_y = cy - text_h / 2 - text_bbox[1]
    draw.multiline_text((text_x, text_y), title, font=font, fill=fill, align="center")


def composite(args: argparse.Namespace) -> None:
    template = Image.open(args.template).convert("RGBA")
    overlay = Image.open(args.overlay).convert("RGBA")

    if not args.no_crop_overlay:
        overlay = trim_transparent(overlay)
    if args.flip_horizontal:
        overlay = overlay.transpose(Image.Transpose.FLIP_LEFT_RIGHT)

    target_width = max(1, int(round(template.width * args.scale)))
    resize_ratio = target_width / overlay.width
    target_height = max(1, int(round(overlay.height * resize_ratio)))
    overlay = overlay.resize((target_width, target_height), Image.Resampling.LANCZOS)

    center_x = int(round(template.width * args.x_frac))
    center_y = int(round(template.height * args.y_frac))
    paste_x = center_x - overlay.width // 2
    paste_y = center_y - overlay.height // 2

    canvas = template.copy()
    canvas.alpha_composite(overlay, (paste_x, paste_y))

    if args.coin_number is not None:
        draw_coin_number(
            canvas,
            args.coin_number,
            x_frac=args.coin_x_frac,
            y_frac=args.coin_y_frac,
            font_size_frac=args.coin_font_size_frac,
            font_path=args.coin_font,
        )

    if args.activation_number is not None:
        draw_centered_text(
            canvas,
            args.activation_number,
            x_frac=args.activation_x_frac,
            y_frac=args.activation_y_frac,
            font_size_frac=args.activation_font_size_frac,
            font_path=args.activation_font,
            font_label="activation-number",
            fill=(255, 255, 255, 255),
        )

    if args.title is not None:
        draw_centered_title_group(
            canvas,
            args.title,
            x_frac=args.title_x_frac,
            y_frac=args.title_y_frac,
            font_size_frac=args.title_font_size_frac,
            font_path=args.title_font,
            fill=parse_hex_color(args.title_color),
            title_icon_path=args.title_icon,
            title_icon_scale=args.title_icon_scale,
            title_icon_gap_px=args.title_icon_gap_px,
            title_icon_y_offset_px=args.title_icon_y_offset_px,
            title_group_offset_x_px=args.title_group_offset_x_px,
            title_group_offset_y_px=args.title_group_offset_y_px,
        )

    if args.bottom_text is not None:
        draw_centered_text(
            canvas,
            args.bottom_text,
            x_frac=args.bottom_text_x_frac,
            y_frac=args.bottom_text_y_frac,
            font_size_frac=args.bottom_text_font_size_frac,
            font_path=args.bottom_text_font,
            font_label="bottom-text",
            fill=parse_hex_color(args.bottom_text_color),
            spacing_px=args.bottom_text_spacing_px,
        )

    args.output.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(args.output)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)

    parser.add_argument("--template", type=Path, required=True, help="Path to card template PNG.")
    parser.add_argument("--overlay", type=Path, required=True, help="Path to floating illustration PNG.")
    parser.add_argument("--output", type=Path, required=True, help="Path for output PNG.")

    # Central illustration
    parser.add_argument("--x-frac", type=float, default=0.50)
    parser.add_argument("--y-frac", type=float, default=0.555)
    parser.add_argument("--scale", type=float, default=0.60)
    parser.add_argument("--flip-horizontal", action="store_true")
    parser.add_argument("--no-crop-overlay", action="store_true")

    # Coin number
    parser.add_argument("--coin-number", type=str, default=None)
    parser.add_argument("--coin-x-frac", type=float, default=0.1594)
    parser.add_argument("--coin-y-frac", type=float, default=0.8836)
    parser.add_argument("--coin-font-size-frac", type=float, default=0.070)
    parser.add_argument("--coin-font", type=Path, default=DEFAULT_COIN_FONT, help="Font file for coin number.")

    # Activation number
    parser.add_argument("--activation-number", type=str, default=None)
    parser.add_argument("--activation-x-frac", type=float, default=0.50)
    parser.add_argument("--activation-y-frac", type=float, default=0.093)
    parser.add_argument("--activation-font-size-frac", type=float, default=0.073)
    parser.add_argument("--activation-font", type=Path, default=DEFAULT_UI_FONT, help="Font file for top activation number.")

    # Title + optional icon
    parser.add_argument("--title", type=str, default=None)
    parser.add_argument("--title-x-frac", type=float, default=0.50, help="Center X of icon+title group.")
    parser.add_argument("--title-y-frac", type=float, default=0.257, help="Center Y of icon+title group.")
    parser.add_argument("--title-font-size-frac", type=float, default=0.052)
    parser.add_argument("--title-font", type=Path, default=DEFAULT_UI_FONT, help="Font file for title.")
    parser.add_argument("--title-color", "--text-color", dest="title_color", type=str, default="#123E70")
    parser.add_argument("--title-icon", type=Path, default=None, help="Optional square icon image before title.")
    parser.add_argument("--title-icon-scale", type=float, default=2.0, help="Icon side / title text height.")
    parser.add_argument("--title-icon-gap-px", type=int, default=10)
    parser.add_argument("--title-icon-y-offset-px", type=int, default=0)
    parser.add_argument("--title-group-offset-x-px", type=int, default=0)
    parser.add_argument("--title-group-offset-y-px", type=int, default=0)

    # Bottom rules text
    parser.add_argument("--bottom-text", type=str, default=None, help="Centered multiline rules text; supports actual newlines, literal \\n, or /n.")
    parser.add_argument("--bottom-text-x-frac", type=float, default=0.50)
    parser.add_argument("--bottom-text-y-frac", type=float, default=0.900)
    parser.add_argument("--bottom-text-font-size-frac", type=float, default=0.030)
    parser.add_argument("--bottom-text-font", type=Path, default=DEFAULT_UI_FONT, help="Font file for bottom rules text.")
    parser.add_argument("--bottom-text-color", type=str, default="#FFFFFF")
    parser.add_argument("--bottom-text-spacing-px", type=int, default=4)

    return parser.parse_args()


if __name__ == "__main__":
    composite(parse_args())
