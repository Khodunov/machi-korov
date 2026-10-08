#!/usr/bin/env bash

set -euo pipefail

.venv/bin/python skills/generate-card/scripts/card_compositor.py \
  --template backgrounds/red.png \
  --overlay buildings/bank-pochta-v2.png \
  --title-icon icons/money-bundle.png \
  --shadow \
  --output cards/bank-pochta.png \
  --x-frac 0.50 \
  --y-frac 0.51 \
  --scale 0.65 \
  --coin-number 0 \
  --activation-number 8 \
  --title 'Банк' \
  --title-color '#58100E' \
  --bottom-text $'При покупке заплатите каждому игроку по 2 монеты.\nВозьмите 2 монеты у бросившего кубики,\nа если собран сет — 4 монеты.\nЕсли у него нет денег, он отдаёт бизнес.' \
  --bottom-text-y-frac 0.815 \
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
  --caption 'Корпорация зла' --caption-font fonts/Boingster-Regular.ttf --caption-font-size-frac 0.026 --caption-x-frac 0.58 --caption-y-frac 0.935 --caption-color '#EDD3CD'
