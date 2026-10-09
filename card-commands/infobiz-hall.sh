#!/usr/bin/env bash

set -euo pipefail

.venv/bin/python skills/generate-card/scripts/card_compositor.py \
  --template backgrounds/red.png \
  --overlay buildings/infobiz-hall.png \
  --title-icon icons/money-bundle.png \
  --shadow \
  --output cards/infobiz-hall.png \
  --x-frac 0.50 \
  --y-frac 0.51 \
  --scale 0.60 \
  --coin-number 1 \
  --activation-number 11 \
  --title 'Инфобизнес' \
  --title-color '#58100E' \
  --bottom-text $'Возьмите 2 монеты у бросившего кубики.\nОн бросает 1 кубик: если выпало 6,\nон забирает эту карточку.' \
  --bottom-text-y-frac 0.815 \
  --bottom-text-spacing-px 5 \
  --title-font fonts/Boingster-Regular.ttf \
  --title-font-size-frac 0.067 \
  --title-icon-scale 1.76 \
  --title-icon-gap-px 12 \
  --title-icon-y-offset-px -8 \
  --bottom-text-font fonts/CCUltimatum-Bold.ttf \
  --bottom-text-font-size-frac 0.031 \
  --activation-font fonts/CCUltimatum-Bold.ttf \
  --activation-font-size-frac 0.118 \
  --coin-font fonts/Boingster-Regular.ttf \
  --caption 'Главное — верить в себя' --caption-font fonts/Boingster-Regular.ttf --caption-font-size-frac 0.026 --caption-x-frac 0.50 --caption-y-frac 0.935 --caption-color '#EDD3CD'
