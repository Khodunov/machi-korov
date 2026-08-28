# Machi Koro Card Compositor

This small toolchain helps assemble custom **Machi Koro-style cards** from reusable pieces:

- a **blank card furniture template** (header, dice, sky, skyline, footer, coin)
- a **floating central illustration** (for example, a panelka building)
- optional **top bar number**
- optional **title**
- optional **icon before the title**
- optional **coin number**
- optional **bottom rules text**

The main script is:

- `composite_machi_koro_card.py`

It composites a transparent PNG illustration onto a template card and draws the configurable text layers on top.

---

## Requirements

- Python 3.10+ recommended
- Dependencies listed in `requirements.txt`

Install dependencies:

```bash
pip install -r requirements.txt
```

Current Python dependency:

- `Pillow`

---

## Files in this setup

### Main script

- `composite_machi_koro_card.py` — composites the artwork and draws text/icon elements.

### Optional/generated assets

Typical inputs:

- a blank card template PNG
- a floating illustration PNG with transparency
- an optional icon PNG with transparency

Typical output:

- a final composed card PNG

---

## What the script can do

### Artwork compositing

- place a floating illustration onto the card
- automatically trim transparent margins from the overlay
- scale the overlay
- move the overlay by configurable normalized coordinates
- optionally flip the overlay horizontally

### Text rendering

- draw a **coin number** inside the bottom-left coin
- draw a **top activation number** in the header
- draw a **top title**
- draw **bottom multiline rules text**
- use separate font files for all 4 text elements

### Title icon support

- optionally place an icon before the title
- center the **icon + title** as one glued horizontal group
- configure icon scale, gap, and fine offsets

---

## Basic usage

```bash
python composite_machi_koro_card.py \
  --template /path/to/template.png \
  --overlay /path/to/building.png \
  --output /path/to/result.png
```

---

## Example matching the current PANELKA card

```bash
python composite_machi_koro_card.py \
  --template backgrounds/blue.png \
  --overlay buildings/panelka.png \
  --output cards/panelka.png \
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
```

---

## CLI arguments

## Required arguments

- `--template` — path to the card template PNG
- `--overlay` — path to the floating illustration PNG
- `--output` — path to the output PNG

---

## Artwork placement

- `--x-frac` — overlay center X as a fraction of card width
- `--y-frac` — overlay center Y as a fraction of card height
- `--scale` — overlay width as a fraction of card width
- `--flip-horizontal` — flip the overlay left-to-right before compositing
- `--no-crop-overlay` — do not trim transparent margins from the overlay before placement

---

## Coin number

- `--coin-number` — single digit `0..9` drawn inside the coin
- `--coin-x-frac` — coin number center X
- `--coin-y-frac` — coin number center Y
- `--coin-font-size-frac` — coin number font size relative to card width
- `--coin-font` — font file path for the coin number

---

## Top activation number

- `--activation-number` — text/number drawn in the top bar
- `--activation-x-frac` — center X of the activation number
- `--activation-y-frac` — center Y of the activation number
- `--activation-font-size-frac` — activation number font size relative to card width
- `--activation-font` — font file path for the activation number

---

## Top title

- `--title` — title text
- `--title-x-frac` — center X of the combined title group
- `--title-y-frac` — center Y of the combined title group
- `--title-font-size-frac` — title font size relative to card width
- `--title-font` — font file path for the title
- `--title-color` — title color in `#RGB` or `#RRGGBB`
- `--text-color` — alias for `--title-color`

---

## Title icon

- `--title-icon` — optional square icon PNG placed before the title
- `--title-icon-scale` — icon size as a multiple of the title text height
- `--title-icon-gap-px` — gap between the icon and the title text
- `--title-icon-y-offset-px` — extra vertical offset for the icon
- `--title-group-offset-x-px` — extra horizontal offset for the combined icon+title group
- `--title-group-offset-y-px` — extra vertical offset for the combined icon+title group

### How the title icon works

If `--title-icon` is provided:

1. the script loads the icon PNG
2. trims its transparent margins
3. rescales it to:
   - `title text height * title-icon-scale`
4. places it before the title
5. centers the full **icon + title** group horizontally as a single unit

This is designed to match the Machi Koro layout where the category badge is visually attached to the title row.

---

## Bottom rules text

- `--bottom-text` — centered multiline bottom text
- `--bottom-text-x-frac` — center X of bottom text
- `--bottom-text-y-frac` — center Y of bottom text
- `--bottom-text-font-size-frac` — bottom text font size relative to card width
- `--bottom-text-font` — font file path for bottom text
- `--bottom-text-color` — bottom text color in `#RGB` or `#RRGGBB`
- `--bottom-text-spacing-px` — line spacing in pixels for multiline text

### Multiline text support

The script accepts:

- actual newlines
- literal `\n`
- accidental `/n`

So all of these are normalized correctly into multiline text.

---

## Font configuration

All 4 text elements support independent font files:

- `--coin-font`
- `--activation-font`
- `--title-font`
- `--bottom-text-font`

Current defaults in the script:

- coin number: `DejaVuSerif-Bold.ttf`
- activation/title/bottom text: `Comfortaa-Bold.ttf`

If you want a different look, just point the corresponding argument to another `.ttf` font file.

---

## Notes on input images

### Template image

The template should already contain the fixed furniture, for example:

- dark blue header with dice
- pale arc
- sky/background
- skyline strip
- footer
- empty coin

### Overlay image

The central illustration should ideally:

- be a PNG with transparency
- contain only the floating object/miniature scene
- avoid any full card background
- avoid extra footer/header elements

### Icon image

The title icon should ideally:

- be a square PNG with transparency
- contain the circular badge or pictogram already prepared
- have some transparent padding so scaling looks clean

---

## Troubleshooting

### 1. Font file not found

If you see a font-related error, check that the provided `--*-font` path exists and points to a valid `.ttf` file.

### 2. Overlay looks misplaced

Adjust:

- `--x-frac`
- `--y-frac`
- `--scale`

### 3. Text looks too large or too small

Adjust the corresponding `--*-font-size-frac` value.

### 4. Bottom text line break isn't working

Use one of these:

```bash
--bottom-text $'Line 1\nLine 2'
```

or pass an actual multiline string from your environment.

---

## Suggested future improvements

Potential next steps:

- subtitle support under the title
- automatic text fitting/shrinking to width
- configurable text bounding boxes
- automatic shadow under the floating illustration
- optional outline/stroke for title and bottom text
- support for multi-digit coin numbers
- preset layout profiles for different card families
- SVG export or vector-first rendering

---

## License / project note

This README only documents the local compositing tool and asset workflow. Any use of visual style inspired by an existing game should be reviewed separately if the project becomes public or commercial.
