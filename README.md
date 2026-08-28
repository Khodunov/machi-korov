# Machi Koro Card Compositor

This repository is a small asset-generation and compositing toolchain for custom **Machi Koro-style cards**. The bundled `$generate-card` skill drives the complete workflow: collecting card parameters, creating prompts, generating artwork, composing a reproducible card, presenting the preview, and iterating on feedback.

## Project structure

```text
card_compositor.py                  # Composites one final card
requirements.txt
backgrounds/                        # Blank card templates by card color
prompts/
  central-illustration.json         # Reusable central-art prompt template
  building-type-icon.json           # Reusable title-icon prompt template
  machi-koro-icon-spec-v1.1.json    # Known-good source specification for round icons
  central-illustrations/
    panelka.json                     # Filled prompt for the panelka artwork
    shwarma-store.json               # Filled prompt for a red-card shawarma shop
  icons/
    house.json                       # Filled prompt for the house icon
    shwarma.json                     # Filled dark-red shawarma icon prompt
buildings/                           # Generated transparent central illustrations
icons/                               # Generated transparent title icons
fonts/                               # Fonts used by card commands
card-commands/
  panelka.sh                         # Reproducible composition settings for one card
  shwarma.sh                         # Red shawarma-card composition settings
cards/                               # Generated final cards; ignored by Git
skills/generate-card/
  SKILL.md                           # End-to-end card creation workflow
  scripts/card_compositor.py         # Compositor used by card commands
```

`prompts/central-illustration.json` and `prompts/building-type-icon.json` are the working templates. Their style, composition, palette, and rendering rules are meant to stay stable. `prompts/machi-koro-icon-spec-v1.1.json` is the known-good source specification from which the icon template is generalized. Copy a working template into the appropriate subdirectory and replace only its `{{CONTENT_PLACEHOLDERS}}` when designing a new asset. The files in `prompts/central-illustrations/` and `prompts/icons/` are filled, generation-ready prompts and provide working examples.

## Requirements

- Python 3.10+
- Pillow, installed from `requirements.txt`

From the repository root:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Creating a card with the skill

Invoke the repository skill in Codex:

```text
Use $generate-card to create a new card.
```

You can include whatever is already decided—for example the title, card color, activation number, cost, effect text, and central subject. The skill asks one concise question for anything important that is still missing, then handles the rest:

1. fills a central-illustration prompt and, when needed, a round category-icon prompt;
2. generates and validates transparent source artwork;
3. creates `card-commands/<card-name>.sh` using the packaged compositor;
4. renders `cards/<card-name>.png` and checks layout, text overflow, transparency, orientation, and forbidden artwork text;
5. presents the card and asks what should be tweaked, rerendering until it is accepted.

Buildings and storefronts are generated already facing slightly right. New commands do not mirror them by default. Central artwork also follows a strict no-text rule: no signs, menus, logos, labels, numbers, pseudo-writing, or other text-like marks.

The full workflow and validation rules live in [`skills/generate-card/SKILL.md`](skills/generate-card/SKILL.md). The reusable JSON files under `prompts/` remain the source templates, while the filled prompt, generated source assets, and card command make each card reproducible.

To regenerate an existing card without creating new artwork, run its command from the repository root:

```bash
bash card-commands/panelka.sh
bash card-commands/shwarma.sh
```

Generated final cards are written under `cards/` and ignored by Git. Commit the filled prompts, generated source artwork, and `card-commands/<card-name>.sh`.

## What the compositor can do

- place, trim, scale, position, and horizontally flip a transparent central illustration
- optionally add a dark half-transparent shadow behind it, shifted equally down and right
- draw the coin number, activation number, title, and multiline rules text
- place an optional icon before the title and center both as one group
- use independent fonts and sizes for each text role

## Direct usage

The skill and per-card shell scripts are the preferred interfaces. For quick experiments, call the packaged compositor directly:

```bash
python skills/generate-card/scripts/card_compositor.py \
  --template backgrounds/blue.png \
  --overlay buildings/panelka.png \
  --title-icon icons/house.png \
  --shadow \
  --output cards/panelka.png
```

## CLI arguments

### Required arguments

- `--template` — path to the card template PNG
- `--overlay` — path to the floating illustration PNG
- `--output` — path to the output PNG

---

### Artwork placement

- `--x-frac` — overlay center X as a fraction of card width
- `--y-frac` — overlay center Y as a fraction of card height
- `--scale` — overlay width as a fraction of card width
- `--flip-horizontal` — flip the overlay left-to-right before compositing
- `--no-crop-overlay` — do not trim transparent margins from the overlay before placement
- `--shadow` — add a dark, half-transparent gray shadow slightly down and right of the central illustration

---

### Coin number

- `--coin-number` — single digit `0..9` drawn inside the coin
- `--coin-x-frac` — coin number center X
- `--coin-y-frac` — coin number center Y
- `--coin-font-size-frac` — coin number font size relative to card width
- `--coin-font` — font file path for the coin number

---

### Top activation number

- `--activation-number` — text/number drawn in the top bar
- `--activation-x-frac` — center X of the activation number
- `--activation-y-frac` — center Y of the activation number
- `--activation-font-size-frac` — activation number font size relative to card width
- `--activation-font` — font file path for the activation number

---

### Top title

- `--title` — title text
- `--title-x-frac` — center X of the combined title group
- `--title-y-frac` — center Y of the combined title group
- `--title-font-size-frac` — title font size relative to card width
- `--title-font` — font file path for the title
- `--title-color` — title color in `#RGB` or `#RRGGBB`
- `--text-color` — alias for `--title-color`

---

### Title icon

- `--title-icon` — optional square icon PNG placed before the title
- `--title-icon-scale` — icon size as a multiple of the title text height
- `--title-icon-gap-px` — gap between the icon and the title text
- `--title-icon-y-offset-px` — extra vertical offset for the icon
- `--title-group-offset-x-px` — extra horizontal offset for the combined icon+title group
- `--title-group-offset-y-px` — extra vertical offset for the combined icon+title group

#### How the title icon works

If `--title-icon` is provided:

1. the script loads the icon PNG
2. trims its transparent margins
3. rescales it to:
   - `title text height * title-icon-scale`
4. places it before the title
5. centers the full **icon + title** group horizontally as a single unit

This is designed to match the Machi Koro layout where the category badge is visually attached to the title row.

---

### Bottom rules text

- `--bottom-text` — centered multiline bottom text
- `--bottom-text-x-frac` — center X of bottom text
- `--bottom-text-y-frac` — center Y of bottom text
- `--bottom-text-font-size-frac` — bottom text font size relative to card width
- `--bottom-text-font` — font file path for bottom text
- `--bottom-text-color` — bottom text color in `#RGB` or `#RRGGBB`
- `--bottom-text-spacing-px` — line spacing in pixels for multiline text

#### Multiline text support

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
- optional outline/stroke for title and bottom text
- support for multi-digit coin numbers
- preset layout profiles for different card families
- SVG export or vector-first rendering

---

## License / project note

This README only documents the local compositing tool and asset workflow. Any use of visual style inspired by an existing game should be reviewed separately if the project becomes public or commercial.
