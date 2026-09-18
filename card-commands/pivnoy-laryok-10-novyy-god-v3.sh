set -euo pipefail

caption=$(.venv/bin/python -c 'import json; print(next(c for c in json.load(open("cards-config.json"))["cards"] if c["slug"] == "pivnoy-laryok")["caption"])')

.venv/bin/python skills/generate-card/scripts/card_compositor.py \
  --template backgrounds/green.png \
  --overlay buildings/pivnoy-laryok-10-novyy-god-v3.png \
  --title-icon icons/shop-stall.png \
  --shadow \
  --output cards/pivnoy-laryok-10-novyy-god-v3.png \
  --x-frac 0.50 \
  --y-frac 0.5250 \
  --scale 0.5953 \
  --coin-number 1 \
  --activation-number '2-3' \
  --title 'Пивной ларёк' \
  --title-color '#17361A' \
  --bottom-text $'Получите 1 монету из банка.\nВ свой ход.' \
  --bottom-text-y-frac 0.82 \
  --bottom-text-spacing-px 6 \
  --title-font fonts/Boingster-Regular.ttf \
  --title-font-size-frac 0.078 \
  --title-icon-scale 1.88 \
  --title-icon-gap-px 12 \
  --title-icon-y-offset-px -10 \
  --bottom-text-font fonts/CCUltimatum-Bold.ttf \
  --bottom-text-font-size-frac 0.0477 \
  --activation-font fonts/CCUltimatum-Bold.ttf \
  --activation-font-size-frac 0.118 \
  --coin-font fonts/Boingster-Regular.ttf \
  --caption "$caption" --caption-font fonts/Boingster-Regular.ttf --caption-font-size-frac 0.026 --caption-x-frac 0.58 --caption-y-frac 0.935 --caption-color '#D8E5C8'
