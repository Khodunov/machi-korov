#!/usr/bin/env bash

set -euo pipefail

.venv/bin/python skills/generate-card/scripts/card_compositor.py \
  --template backgrounds/red.png \
  --overlay buildings/bukmekerskaya-kontora-v2-1xbet.png \
  --title-icon icons/gambling-chip.png \
  --shadow \
  --output cards/bukmekerskaya-kontora.png \
  --x-frac 0.50 \
  --y-frac 0.51 \
  --scale 0.64 \
  --coin-number 3 \
  --activation-number 7 \
  --title 'Букмекерская контора' \
  --title-color '#58100E' \
  --bottom-text $'Попавший выбирает число от 1 до 6\nи бросает кубик.\nЕсли число выпало, контора платит ему 2 монеты.\nЕсли не выпало, он платит конторе 3 монеты.' \
  --bottom-text-y-frac 0.835 \
  --bottom-text-spacing-px 5 \
  --title-font fonts/Boingster-Regular.ttf \
  --title-font-size-frac 0.058 \
  --title-icon-scale 1.55 \
  --title-icon-gap-px 10 \
  --title-icon-y-offset-px -5 \
  --bottom-text-font fonts/CCUltimatum-Bold.ttf \
  --bottom-text-font-size-frac 0.030 \
  --activation-font fonts/CCUltimatum-Bold.ttf \
  --activation-font-size-frac 0.118 \
  --coin-font fonts/Boingster-Regular.ttf
