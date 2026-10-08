#!/usr/bin/env bash

set -euo pipefail

.venv/bin/python skills/generate-card/scripts/card_compositor.py \
  --template backgrounds/red.png \
  --overlay buildings/lombard-reference-v2-winter.png \
  --title-icon icons/money-bundle.png \
  --shadow \
  --output cards/lombard.png \
  --x-frac 0.50 \
  --y-frac 0.51 \
  --scale 0.59 \
  --coin-number 0 \
  --activation-number 2 \
  --title 'Ломбард' \
  --title-color '#58100E' \
  --bottom-text $'При покупке платишь всем по 1 монете.\nПопавший платит 1 монету.\nЕсли собран сет, то платит 2.\nЕсли не хватает, то отдаёт бизнес.' \
  --bottom-text-y-frac 0.835 \
  --bottom-text-spacing-px 5 \
  --title-font fonts/Boingster-Regular.ttf \
  --title-font-size-frac 0.084 \
  --title-icon-scale 1.76 \
  --title-icon-gap-px 12 \
  --title-icon-y-offset-px -8 \
  --bottom-text-font fonts/CCUltimatum-Bold.ttf \
  --bottom-text-font-size-frac 0.031 \
  --activation-font fonts/CCUltimatum-Bold.ttf \
  --activation-font-size-frac 0.118 \
  --coin-font fonts/Boingster-Regular.ttf \
  --caption 'Сюда ты понесешь свое обручальное кольцо' --caption-font fonts/Boingster-Regular.ttf --caption-font-size-frac 0.026 --caption-x-frac 0.50 --caption-y-frac 0.935 --caption-color '#EDD3CD'
