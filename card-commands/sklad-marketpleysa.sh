#!/usr/bin/env bash

set -euo pipefail

caption=$(.venv/bin/python -c 'import json; print(next(c for c in json.load(open("cards-config.json"))["cards"] if c["slug"] == "sklad-marketpleysa")["caption"])')

.venv/bin/python skills/generate-card/scripts/card_compositor.py \
  --template backgrounds/green.png \
  --overlay buildings/sklad-marketpleysa-v3-wildberries-explosion-v2.png \
  --title-icon icons/pvz-v3.png \
  --shadow \
  --output cards/sklad-marketpleysa.png \
  --x-frac 0.50 \
  --y-frac 0.51 \
  --scale 0.86 \
  --coin-number 2 \
  --activation-number 9 \
  --title 'Склад маркетплейса' \
  --title-color '#17361A' \
  --bottom-text $'Получите 1 монету из банка и ещё\nпо 1 монете за каждый свой «ПВЗ».\nВ свой ход.' \
  --bottom-text-y-frac 0.82 \
  --bottom-text-spacing-px 5 \
  --title-font fonts/Boingster-Regular.ttf \
  --title-font-size-frac 0.055 \
  --title-icon-scale 1.68 \
  --title-icon-gap-px 10 \
  --title-icon-y-offset-px -8 \
  --bottom-text-font fonts/CCUltimatum-Bold.ttf \
  --bottom-text-font-size-frac 0.038 \
  --activation-font fonts/CCUltimatum-Bold.ttf \
  --activation-font-size-frac 0.118 \
  --coin-font fonts/Boingster-Regular.ttf \
  --caption "$caption" \
  --caption-font fonts/Boingster-Regular.ttf \
  --caption-font-size-frac 0.026 \
  --caption-x-frac 0.50 \
  --caption-y-frac 0.935 \
  --caption-color '#D8E5C8'
