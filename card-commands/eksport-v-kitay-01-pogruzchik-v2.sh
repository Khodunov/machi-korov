set -euo pipefail

caption=$(.venv/bin/python -c 'import json; print(next(c for c in json.load(open("cards-config.json"))["cards"] if c["slug"] == "eksport-v-kitay")["caption"])')

.venv/bin/python skills/generate-card/scripts/card_compositor.py \
  --template backgrounds/green.png \
  --overlay buildings/eksport-v-kitay-01-pogruzchik-v2.png \
  --title-icon icons/factory-green.png \
  --shadow \
  --output cards/eksport-v-kitay-01-pogruzchik-v2.png \
  --x-frac 0.50 \
  --y-frac 0.515 \
  --scale 0.80 \
  --coin-number 3 \
  --activation-number 8 \
  --title 'Экспорт в Китай' \
  --title-color '#17361A' \
  --bottom-text $'Получите по 3 монеты за каждый\nсвой «Лесоповал» и «НПЗ».\nВ свой ход.' \
  --bottom-text-y-frac 0.82 \
  --bottom-text-spacing-px 6 \
  --title-font fonts/Boingster-Regular.ttf \
  --title-font-size-frac 0.078 \
  --title-icon-scale 1.88 \
  --title-icon-gap-px 12 \
  --title-icon-y-offset-px -10 \
  --bottom-text-font fonts/CCUltimatum-Bold.ttf \
  --bottom-text-font-size-frac 0.043 \
  --activation-font fonts/CCUltimatum-Bold.ttf \
  --activation-font-size-frac 0.118 \
  --coin-font fonts/Boingster-Regular.ttf \
  --caption "$caption" --caption-font fonts/Boingster-Regular.ttf --caption-font-size-frac 0.026 --caption-x-frac 0.58 --caption-y-frac 0.935 --caption-color '#D8E5C8'
