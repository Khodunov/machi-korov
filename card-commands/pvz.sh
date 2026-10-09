#!/usr/bin/env bash
set -euo pipefail

caption=$(.venv/bin/python -c 'import json; print(next(c for c in json.load(open("cards-config.json"))["cards"] if c["slug"] == "pvz")["caption"])')

.venv/bin/python skills/generate-card/scripts/card_compositor.py \
  --template backgrounds/blue.png \
  --overlay buildings/pvz-yandex-market-brick-v3.png \
  --title-icon icons/pvz-v3.png \
  --shadow \
  --output cards/pvz.png \
  --x-frac 0.50 \
  --y-frac 0.49 \
  --scale 0.72 \
  --coin-number 2 \
  --activation-number 3 \
  --title 'ПВЗ' \
  --title-color '#123E70' \
  --bottom-text $'Получите 1 монету из банка.\nВ ход любого игрока.' \
  --bottom-text-y-frac 0.83 \
  --bottom-text-spacing-px 6 \
  --title-font fonts/Boingster-Regular.ttf \
  --title-font-size-frac 0.078 \
  --title-icon-scale 1.88 \
  --title-icon-gap-px 12 \
  --title-icon-y-offset-px -10 \
  --bottom-text-font fonts/CCUltimatum-Bold.ttf \
  --bottom-text-font-size-frac 0.05 \
  --activation-font fonts/CCUltimatum-Bold.ttf \
  --activation-font-size-frac 0.118 \
  --coin-font fonts/Boingster-Regular.ttf \
  --caption "$caption" --caption-font fonts/Boingster-Regular.ttf --caption-font-size-frac 0.026 --caption-x-frac 0.50 --caption-y-frac 0.935 --caption-color '#D9E8F3'
