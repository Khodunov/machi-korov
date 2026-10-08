#!/usr/bin/env python3
"""Generate the shared Machi Koro-style card back.

Neutral graphite palette, flat schematic Russian city panorama:
Orthodox church, Moscow City tower cluster, a shopping mall, panel blocks,
a TV needle and courtyard garages, layered in three depth tones.

The card silhouette (size, rounded corners, cream surround) is matched to
backgrounds/*.png so the back registers exactly with the card fronts.

Run from the repository root:
    python card-back/generate_card_back.py
"""

from __future__ import annotations

import math
from pathlib import Path

from PIL import Image, ImageChops, ImageDraw, ImageFilter

# --- Card geometry, measured from backgrounds/blue.png -----------------------
CANVAS = (1100, 1430)
CARD_BOX = (50, 31, 1059, 1406)  # x0, y0, x1, y1
CORNER_RADIUS = 71
CREAM = (252, 249, 241)

SS = 3  # supersampling factor

# --- Neutral palette ---------------------------------------------------------
P = {
    "header": (54, 58, 64),
    "dice": (72, 77, 84),
    "arc": (222, 221, 215),
    "sky_top": (206, 207, 203),
    "sky_bot": (176, 179, 179),
    "cloud": (238, 237, 230),
    "far": (150, 154, 157),
    "mid": (112, 117, 122),
    "near": (80, 85, 91),
    "fore": (60, 65, 71),
    "footer": (44, 48, 54),
    "window": (228, 193, 126),
    "window_off": (96, 101, 107),
    "gold": (214, 178, 108),
}


def s(v: float) -> int:
    """Scale a card-space value into the supersampled buffer."""
    return int(round(v * SS))


# ---------------------------------------------------------------------------
# Shape helpers
# ---------------------------------------------------------------------------


def vertical_gradient(size, top, bottom):
    w, h = size
    grad = Image.new("RGB", (1, h))
    px = grad.load()
    for y in range(h):
        t = y / max(h - 1, 1)
        px[0, y] = tuple(round(top[i] + (bottom[i] - top[i]) * t) for i in range(3))
    return grad.resize((w, h), Image.BILINEAR)


def window_grid(d, x, y, w, h, cols, rows, color, lit=(), pad=0.28):
    """Simplified rectangular window grid, a few cells optionally lit."""
    if cols <= 0 or rows <= 0:
        return
    cw = w / cols
    ch = h / rows
    ww = cw * (1 - pad)
    wh = ch * (1 - pad)
    for r in range(rows):
        for c in range(cols):
            cx = x + cw * c + (cw - ww) / 2
            cy = y + ch * r + (ch - wh) / 2
            fill = P["window"] if (c, r) in lit else color
            d.rectangle([cx, cy, cx + ww, cy + wh], fill=fill)


def onion_dome(d, cx, base_y, w, h, color, cross=True):
    """Schematic onion dome: bulged body, pointed tip, small cross."""
    half = w / 2
    pts = []
    steps = 36
    for i in range(steps + 1):
        t = i / steps
        # profile: wide belly near the bottom, pinched tip at the top
        y = base_y - h * t
        bulge = math.sin(math.pi * (t ** 0.72)) * 1.0
        taper = (1 - t) ** 0.35
        r = half * (0.42 + 0.58 * bulge) * (0.35 + 0.65 * taper)
        pts.append((cx + r, y))
    for i in range(steps, -1, -1):
        t = i / steps
        y = base_y - h * t
        bulge = math.sin(math.pi * (t ** 0.72)) * 1.0
        taper = (1 - t) ** 0.35
        r = half * (0.42 + 0.58 * bulge) * (0.35 + 0.65 * taper)
        pts.append((cx - r, y))
    d.polygon(pts, fill=color)
    if cross:
        cw = w * 0.30
        cy = base_y - h
        bar = max(s(1.2), 2)
        d.rectangle([cx - bar / 2, cy - cw * 1.15, cx + bar / 2, cy], fill=color)
        d.rectangle([cx - cw * 0.36, cy - cw * 0.80, cx + cw * 0.36, cy - cw * 0.80 + bar],
                    fill=color)


def church(d, cx, base_y, scale, color, accent):
    """Orthodox church: central drum + dome, four small domes, bell tower."""
    u = scale
    body_w = 5.6 * u
    body_h = 3.0 * u
    d.rectangle([cx - body_w / 2, base_y - body_h, cx + body_w / 2, base_y], fill=color)

    # apse
    d.rectangle([cx + body_w / 2, base_y - body_h * 0.68,
                 cx + body_w / 2 + 1.0 * u, base_y], fill=color)

    # central drum + dome
    drum_w = 1.7 * u
    drum_h = 1.7 * u
    drum_y = base_y - body_h
    d.rectangle([cx - drum_w / 2, drum_y - drum_h, cx + drum_w / 2, drum_y], fill=color)
    onion_dome(d, cx, drum_y - drum_h, 2.0 * u, 1.9 * u, accent)

    # two flanking small domes
    for off in (-1.9 * u, 1.9 * u):
        sd_w = 0.85 * u
        sd_h = 0.95 * u
        sy = base_y - body_h
        d.rectangle([cx + off - sd_w / 2, sy - sd_h, cx + off + sd_w / 2, sy], fill=color)
        onion_dome(d, cx + off, sy - sd_h, 1.05 * u, 1.0 * u, accent)

    # bell tower on the left
    bt_w = 1.5 * u
    bt_h = 5.0 * u
    bt_x = cx - body_w / 2 - bt_w
    d.rectangle([bt_x, base_y - bt_h, bt_x + bt_w, base_y], fill=color)
    d.rectangle([bt_x + bt_w * 0.28, base_y - bt_h * 0.86,
                 bt_x + bt_w * 0.72, base_y - bt_h * 0.60], fill=accent)
    onion_dome(d, bt_x + bt_w / 2, base_y - bt_h, 1.35 * u, 1.5 * u, accent)

    # arched windows on the body
    for i in range(3):
        wx = cx - body_w * 0.30 + i * body_w * 0.30
        d.rectangle([wx - 0.20 * u, base_y - body_h * 0.66,
                     wx + 0.20 * u, base_y - body_h * 0.20], fill=accent)


def federation_tower(d, x, base_y, w, h, color):
    """Tapered twin spire."""
    d.polygon([(x, base_y), (x + w, base_y),
               (x + w * 0.74, base_y - h), (x + w * 0.26, base_y - h)], fill=color)
    spire = max(s(2.0), 3)
    d.rectangle([x + w / 2 - spire / 2, base_y - h * 1.16,
                 x + w / 2 + spire / 2, base_y - h], fill=color)


def twisted_tower(d, x, base_y, w, h, color, turns=0.55, segments=16):
    """Evolution-style twist, approximated as a stack of sheared slabs."""
    seg_h = h / segments
    for i in range(segments):
        t = i / (segments - 1)
        y0 = base_y - seg_h * (i + 1)
        y1 = base_y - seg_h * i
        a = math.sin(t * math.pi * turns * 2) * w * 0.20
        b = math.sin((t + 1 / segments) * math.pi * turns * 2) * w * 0.20
        d.polygon([(x + a, y1), (x + w + a, y1), (x + w + b, y0), (x + b, y0)], fill=color)


def stepped_tower(d, x, base_y, w, h, color, steps=3):
    """OKO/Mercury-style setbacks."""
    cur_w = w
    cur_x = x
    seg = h / steps
    for i in range(steps):
        d.rectangle([cur_x, base_y - seg * (i + 1), cur_x + cur_w, base_y - seg * i],
                    fill=color)
        cur_x += cur_w * 0.13
        cur_w *= 0.74


def shopping_mall(d, x, base_y, w, h, color, accent):
    """Wide low retail box with a barrel-vault roof and a glazed entrance."""
    body_h = h * 0.66
    top = base_y - body_h
    roof_h = h * 0.34
    # barrel roof, seated exactly on the body
    d.pieslice([x, top - roof_h, x + w, top + roof_h], 180, 360, fill=color)
    d.rectangle([x, top, x + w, base_y], fill=color)
    # glazing band along the facade
    band_y = top + body_h * 0.24
    d.rectangle([x + w * 0.06, band_y, x + w * 0.94, band_y + body_h * 0.20], fill=accent)
    mull = max(s(1.3), 2)
    for i in range(1, 8):
        mx = x + w * 0.06 + (w * 0.88) * i / 8
        d.rectangle([mx - mull / 2, band_y, mx + mull / 2, band_y + body_h * 0.20],
                    fill=color)
    # entrance
    d.rectangle([x + w * 0.40, base_y - body_h * 0.42, x + w * 0.60, base_y], fill=accent)


def lollipop_tree(d, cx, base_y, h, color):
    """Round tree silhouette, matching the skyline strip on the card fronts."""
    trunk = max(h * 0.10, s(1.6))
    crown_r = h * 0.34
    d.rectangle([cx - trunk / 2, base_y - h * 0.72, cx + trunk / 2, base_y], fill=color)
    d.ellipse([cx - crown_r, base_y - h, cx + crown_r, base_y - h + crown_r * 2], fill=color)


def panel_block(d, x, base_y, w, h, color, cols, rows, win, lit=()):
    d.rectangle([x, base_y - h, x + w, base_y], fill=color)
    window_grid(d, x + w * 0.10, base_y - h * 0.90, w * 0.80, h * 0.80, cols, rows, win, lit)


def tv_tower(d, cx, base_y, h, color):
    """Ostankino-style needle."""
    base_w = h * 0.115
    d.polygon([(cx - base_w, base_y), (cx + base_w, base_y),
               (cx + base_w * 0.16, base_y - h * 0.72),
               (cx - base_w * 0.16, base_y - h * 0.72)], fill=color)
    pod = base_w * 0.62
    d.rectangle([cx - pod, base_y - h * 0.78, cx + pod, base_y - h * 0.70], fill=color)
    needle = max(s(1.6), 2)
    d.rectangle([cx - needle / 2, base_y - h, cx + needle / 2, base_y - h * 0.72], fill=color)


def cloud(d, cx, cy, w, color):
    h = w * 0.40
    d.ellipse([cx - w / 2, cy - h / 2, cx - w * 0.06, cy + h / 2], fill=color)
    d.ellipse([cx - w * 0.26, cy - h * 0.80, cx + w * 0.28, cy + h / 2], fill=color)
    d.ellipse([cx + w * 0.06, cy - h * 0.40, cx + w / 2, cy + h / 2], fill=color)
    d.rectangle([cx - w * 0.40, cy + h * 0.10, cx + w * 0.40, cy + h / 2], fill=color)


def die(d, cx, cy, size, pips, color, pip_color):
    r = size * 0.22
    d.rounded_rectangle([cx - size / 2, cy - size / 2, cx + size / 2, cy + size / 2],
                        radius=r, fill=color)
    step = size * 0.26
    layouts = {
        1: [(0, 0)],
        2: [(-1, -1), (1, 1)],
        3: [(-1, -1), (0, 0), (1, 1)],
        4: [(-1, -1), (1, -1), (-1, 1), (1, 1)],
        5: [(-1, -1), (1, -1), (0, 0), (-1, 1), (1, 1)],
        6: [(-1, -1), (1, -1), (-1, 0), (1, 0), (-1, 1), (1, 1)],
    }
    pr = size * 0.085
    for dx, dy in layouts[pips]:
        d.ellipse([cx + dx * step - pr, cy + dy * step - pr,
                   cx + dx * step + pr, cy + dy * step + pr], fill=pip_color)


# ---------------------------------------------------------------------------
# Card back
# ---------------------------------------------------------------------------


def build_card_face(w: int, h: int) -> Image.Image:
    """Draw the card interior at supersampled resolution."""
    img = vertical_gradient((w, h), P["sky_top"], P["sky_bot"]).convert("RGB")
    d = ImageDraw.Draw(img)

    header_h = h * 0.155
    ground_y = h * 0.918

    # --- header band with dice, echoing the card fronts -------------------
    d.rectangle([0, 0, w, header_h], fill=P["header"])
    for fx, fy, fs, pips in [
        (0.09, 0.52, 0.120, 3), (0.26, 0.30, 0.140, 5), (0.44, 0.62, 0.105, 2),
        (0.61, 0.28, 0.135, 6), (0.79, 0.56, 0.115, 4), (0.94, 0.26, 0.100, 1),
    ]:
        die(d, w * fx, header_h * fy, w * fs, pips, P["dice"], P["header"])
    d.rectangle([0, header_h, w, header_h], fill=P["header"])

    # --- thin pale arc under the header, drawn as a crescent mask ---------
    outer_box = [-w * 0.32, header_h - h * 0.010, w * 1.32, header_h + h * 0.300]
    inner_box = [-w * 0.32, header_h + h * 0.042, w * 1.32, header_h + h * 0.352]
    outer = Image.new("L", (w, h), 0)
    ImageDraw.Draw(outer).pieslice(outer_box, 180, 360, fill=255)
    inner = Image.new("L", (w, h), 0)
    ImageDraw.Draw(inner).pieslice(inner_box, 180, 360, fill=255)
    img.paste(Image.new("RGB", (w, h), P["arc"]), (0, 0), ImageChops.subtract(outer, inner))

    # --- clouds -----------------------------------------------------------
    for cx, cy, cw in [(0.155, 0.295, 0.150), (0.865, 0.268, 0.130),
                       (0.335, 0.395, 0.098), (0.955, 0.430, 0.085),
                       (0.470, 0.330, 0.078), (0.735, 0.318, 0.100)]:
        cloud(d, w * cx, h * cy, w * cw, P["cloud"])

    # =====================================================================
    # City panorama — three depth layers, far to near
    # =====================================================================

    # --- FAR layer: TV needle, distant slabs, Moscow City cluster ---------
    far_base = h * 0.700
    tv_tower(d, w * 0.088, far_base, h * 0.320, P["far"])
    for x0, ww, hh in [(0.155, 0.052, 0.142), (0.220, 0.044, 0.110),
                       (0.400, 0.050, 0.125), (0.462, 0.040, 0.098)]:
        d.rectangle([w * x0, far_base - h * hh, w * (x0 + ww), far_base], fill=P["far"])

    federation_tower(d, w * 0.518, far_base, w * 0.086, h * 0.360, P["far"])
    twisted_tower(d, w * 0.616, far_base, w * 0.066, h * 0.266, P["far"])
    stepped_tower(d, w * 0.692, far_base, w * 0.080, h * 0.300, P["far"], steps=3)
    d.rectangle([w * 0.783, far_base - h * 0.206, w * 0.836, far_base], fill=P["far"])
    federation_tower(d, w * 0.846, far_base, w * 0.060, h * 0.247, P["far"])
    d.rectangle([w * 0.916, far_base - h * 0.178, w * 0.966, far_base], fill=P["far"])

    # --- MID layer: church hero + panel blocks ----------------------------
    mid_base = h * 0.800
    church(d, w * 0.248, mid_base, w * 0.0390, P["mid"], P["gold"])

    # keep 0.08-0.38 clear so the church silhouette reads uncluttered
    panel_block(d, w * 0.386, mid_base, w * 0.112, h * 0.182, P["mid"], 4, 6,
                P["window_off"], lit={(1, 1), (3, 4), (0, 3)})
    panel_block(d, w * 0.510, mid_base, w * 0.088, h * 0.137, P["mid"], 3, 5,
                P["window_off"], lit={(2, 0), (0, 2)})
    panel_block(d, w * 0.610, mid_base, w * 0.126, h * 0.163, P["mid"], 5, 5,
                P["window_off"], lit={(4, 1), (1, 3), (2, 3)})
    panel_block(d, w * 0.750, mid_base, w * 0.082, h * 0.118, P["mid"], 3, 4,
                P["window_off"], lit={(1, 2)})
    panel_block(d, w * 0.856, mid_base, w * 0.100, h * 0.130, P["mid"], 4, 4,
                P["window_off"], lit={(2, 2)})

    # --- NEAR layer: shopping mall + low blocks ---------------------------
    near_base = h * 0.868
    shopping_mall(d, w * 0.596, near_base, w * 0.260, h * 0.150, P["near"], P["window_off"])
    panel_block(d, w * 0.392, near_base, w * 0.104, h * 0.101, P["near"], 4, 3,
                P["window_off"], lit={(1, 1)})
    panel_block(d, w * 0.872, near_base, w * 0.118, h * 0.120, P["near"], 5, 4,
                P["window_off"], lit={(2, 0), (4, 2)})
    d.rectangle([w * 0.506, near_base - h * 0.062, w * 0.580, near_base], fill=P["near"])
    d.rectangle([-w * 0.010, near_base - h * 0.067, w * 0.068, near_base], fill=P["near"])

    # --- FOREGROUND: garage row, kiosk, trees, ground band ----------------
    d.rectangle([0, ground_y, w, h], fill=P["footer"])

    gx = w * 0.040
    for i in range(6):
        x = gx + i * w * 0.049
        d.rectangle([x, ground_y - h * 0.040, x + w * 0.043, ground_y], fill=P["fore"])
        d.rectangle([x + w * 0.007, ground_y - h * 0.027,
                     x + w * 0.036, ground_y], fill=P["footer"])

    kx = w * 0.372
    d.rectangle([kx, ground_y - h * 0.050, kx + w * 0.072, ground_y], fill=P["fore"])
    d.rectangle([kx + w * 0.009, ground_y - h * 0.038,
                 kx + w * 0.063, ground_y - h * 0.016], fill=P["window"])

    d.rectangle([w * 0.616, ground_y - h * 0.036, w * 0.760, ground_y], fill=P["fore"])
    d.rectangle([w * 0.836, ground_y - h * 0.030, w * 0.960, ground_y], fill=P["fore"])

    for tx, th in [(0.336, 0.052), (0.556, 0.058), (0.588, 0.044), (0.800, 0.055)]:
        lollipop_tree(d, w * tx, ground_y, h * th, P["fore"])

    return img


def main() -> None:
    w, h = CANVAS
    x0, y0, x1, y1 = CARD_BOX
    card_w, card_h = x1 - x0, y1 - y0

    face = build_card_face(s(card_w), s(card_h))

    # rounded-corner mask matching the fronts
    mask = Image.new("L", (s(card_w), s(card_h)), 0)
    ImageDraw.Draw(mask).rounded_rectangle(
        [0, 0, s(card_w) - 1, s(card_h) - 1], radius=s(CORNER_RADIUS), fill=255
    )

    face = face.resize((card_w, card_h), Image.LANCZOS)
    mask = mask.resize((card_w, card_h), Image.LANCZOS)

    out = Image.new("RGB", (w, h), CREAM)

    # soft drop shadow under the card, as on the fronts
    shadow = Image.new("L", (w, h), 0)
    ImageDraw.Draw(shadow).rounded_rectangle(
        [x0 + 3, y0 + 6, x1 + 3, y1 + 6], radius=CORNER_RADIUS, fill=90
    )
    shadow = shadow.filter(ImageFilter.GaussianBlur(9))
    out.paste(Image.new("RGB", (w, h), (176, 170, 158)), (0, 0), shadow)

    out.paste(face, (x0, y0), mask)

    dest = Path("cards/card-back.png")
    dest.parent.mkdir(parents=True, exist_ok=True)
    out.save(dest, "PNG", dpi=(300, 300))
    print(f"Wrote {dest} ({out.size[0]}x{out.size[1]}, 300 dpi)")


if __name__ == "__main__":
    main()
