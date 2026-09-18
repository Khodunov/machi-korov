set -euo pipefail

caption=$(.venv/bin/python -c 'import json; print(next(c for c in json.load(open("cards-config.json"))["cards"] if c["slug"] == "novostroyka")["caption"])')

.venv/bin/python skills/generate-card/scripts/card_compositor.py \
  --template backgrounds/blue.png \
  --overlay buildings/novostroyka-01-murino-stena.png \
  --title-icon icons/house.png \
  --shadow \
  --output cards/novostroyka-01-murino-stena.png \
  --x-frac 0.50 \
  --y-frac 0.505 \
  --scale 0.5524 \
  --coin-number 3 \
  --activation-number 10 \
  --title 'Новостройка' \
  --title-color '#123E70' \
  --bottom-text $'Получите 3 монеты за ЖКХ.\nВ ход любого игрока.' \
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
  --caption "$caption" --caption-font fonts/Boingster-Regular.ttf --caption-font-size-frac 0.026 --caption-x-frac 0.58 --caption-y-frac 0.935 --caption-color "#D9E8F3"
