set -euo pipefail

caption=$(.venv/bin/python -c 'import json; print(next(c for c in json.load(open("cards-config.json"))["cards"] if c["slug"] == "autoservice")["caption"])')

.venv/bin/python skills/generate-card/scripts/card_compositor.py \
  --template backgrounds/green.png \
  --overlay buildings/autoservice-01-petrovich.png \
  --title-icon icons/shop-stall.png \
  --shadow \
  --output cards/autoservice-01-petrovich.png \
  --x-frac 0.50 \
  --y-frac 0.51 \
  --scale 0.72 \
  --coin-number 5 \
  --activation-number '7' \
  --title 'Автосервис' \
  --title-color '#17361A' \
  --bottom-text $'Получите по 3 монеты\nза каждый свой гараж.\nВ свой ход.' \
  --bottom-text-y-frac 0.815 \
  --bottom-text-spacing-px 6 \
  --title-font fonts/Boingster-Regular.ttf \
  --title-font-size-frac 0.078 \
  --title-icon-scale 1.88 \
  --title-icon-gap-px 12 \
  --title-icon-y-offset-px -10 \
  --bottom-text-font fonts/CCUltimatum-Bold.ttf \
  --bottom-text-font-size-frac 0.0366 \
  --activation-font fonts/CCUltimatum-Bold.ttf \
  --activation-font-size-frac 0.118 \
  --coin-font fonts/Boingster-Regular.ttf \
  --caption "$caption" --caption-font fonts/Boingster-Regular.ttf --caption-font-size-frac 0.026 --caption-x-frac 0.58 --caption-y-frac 0.935 --caption-color "#D8E5C8"
