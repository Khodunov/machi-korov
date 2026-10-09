# Landmark layout

Use for достопримечательности / landmarks. The current layout is a first reusable
adaptation of the original game's two-state cards, pending the user's visual refinements.

## Reference and design choices

Original-game rules: https://www.yucata.de/en/Rules/MachiKoro
Visual example of both sides: https://www.yucata.de/game-plugins/machikoro/1.0.3/images/turnedBiggie.png
Publisher rulebook: https://www.gokids.com.tw/tsaiss/gokids/rules/MK%20BASE%20RULE%20EN.pdf

The original has no activation number; title above the artwork, effect below it,
and construction cost at lower left. The same landmark is shown on the unbuilt and
built sides. An unbuilt card is muted and marked for construction; completing it
turns it to the full-color side. It does not use the shared establishment back.

Our adaptation uses a gold sky and brown footer when built, a gray-green palette
when unbuilt, and the original large construction-machine triangle layered over
the artwork. Reuse `icons/landmark-construction-original.png` (transparent PNG)
or its SVG; never regenerate or replace it with an exclamation mark or text label.
The original vector paths were extracted from PDF page 7 of
https://cdn.1j1ju.com/medias/89/cb/e8-machi-koro-rulebook.pdf . Provenance is in
`references/landmark-construction-source.json`; the reproducible extraction script
is `scripts/extract_landmark_construction.py` (PyMuPDF required only for extraction).

Every landmark uses `icons/landmark.png` / `.svg` beside its title: the original
white monument in a round badge. This is one shared asset, not a per-card generation.
Place the title and badge directly over the continuous sky/artwork background;
do not draw a separate header panel, band, or divider behind them.
The compositor centers icon and title together and mutes the badge on the unbuilt side.
Do not add an activation number, dice header, flavor caption or a new reverse
illustration by default. Title, effect and price remain readable on both sides.

The construction sign is a separate RGBA layer. Its default width is 46% of card
width, centered at (512, 685). `--construction-icon` selects its source and
`--construction-width-frac` controls its size. `--output-construction-layer` saves
an independent 1024 × 1536 transparent overlay, directly reusable over any card
with this layout. The demo exports `icons/landmark-construction-layer.png`.
`--title-icon` overrides the shared badge only if requested.

## Geometry

Both sides are 1024 × 1536, matching existing templates. Rounded card bounds:
(76, 30)–(948, 1500). Title box: (118, 73)–(906, 228). Illustration: fit within
710 × 710, centered at (512, 655), trimmed once and placed identically on both sides.
Footer begins at Y=1145 and ends at Y=1500. Rules box:
(118, 1165)–(906, 1480). The complete visible text/icon block is centered
at Y=1322.5, the vertical midpoint of the footer, and X=512.
The original 134 px cost coin sits at (111, 1325)–(245, 1459), centered
at (178, 1392), with its original 76 px price font.
Text fitting preserves the footer midpoint. Each line is centered by its
visible ink bounds, including inline badges, then shifted right only if needed
to flow around the circular coin with 14 px clearance. Lines above the coin
remain centered on the card; never reserve a top-only strip for effects.
Rules support `{shop}` (the shared shop-stall badge) and `{restaurant}`
(the shared glass-and-fork badge). For the shopping mall use three lines:
`Каждое ваше предприятие\nс символом {shop} или {restaurant}\nприносит на 1 монету больше.`
Use up to three deliberate lines for current landmark effects; both states keep
the same effect layout and category badge colors.
The compositor bounds text and shrinks it only to readable minimum sizes; overflow
raises an error. Add deliberate line breaks or shorten text rather than shrinking
the whole card. Price accepts integers 0–99; establishment price behavior is unchanged.

The code draws the layout deterministically; blank exports under
`backgrounds/landmark-front.png` and `backgrounds/landmark-back.png` are previews
of the furniture, not independent editable source templates. Edit the compositor
to change the layout, then regenerate the exports and specimen.

## Paired card command

From the repository root, save a command in `card-commands/<slug>.sh`:

```bash
.venv/bin/python skills/generate-card/scripts/landmark_compositor.py \
  --overlay buildings/<slug>.png \
  --title 'Название' \
  --rules $'Первая строка эффекта.\nВторая строка.' \
  --cost 22 \
  --output-front cards/<slug>.png \
  --output-back card-backs/<slug>.png \
  --preview cards/<slug>-preview.png
```

Obtain title, exact effect, cost and subject from the user before creating a real
card. Use the existing central-illustration prompt and no-text/transparent-art
requirements. Generate only one illustration; the compositor derives the muted
version while preserving alpha. Do not independently regenerate the back.
Do not overwrite existing artwork unless requested.

Run `bash -n` and execute the command. Inspect the pair for text fit, cost centering,
identical artwork registration and legible construction status. Deliver both PNGs
and the paired preview. Each landmark gets its own back, even when several share
the same cost or effect. Print front and back at identical dimensions without mirroring
the artwork; duplex page imposition is a separate task.

`card-commands/landmark-layout-demo.sh` regenerates the layout specimen and blank
exports using existing panelka artwork as a placeholder. Its cost and text are
demonstration content, not a finalized game card.
