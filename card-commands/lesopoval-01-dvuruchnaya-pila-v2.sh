set -euo pipefail

caption=$(.venv/bin/python -c 'import json; print(next(c for c in json.load(open("cards-config.json"))["cards"] if c["slug"] == "lesopoval")["caption"])')

.venv/bin/python skills/generate-card/scripts/card_compositor.py \
  --template backgrounds/blue.png \
  --overlay buildings/lesopoval-01-dvuruchnaya-pila-v2.png \
  --title-icon icons/resources.png \
  --shadow \
  --output cards/lesopoval-01-dvuruchnaya-pila-v2.png \
  --x-frac 0.49 \
  --y-frac 0.535 \
  --scale 0.66 \
  --coin-number 3 \
  --activation-number 5 \
  --title 'Лесоповал' \
  --title-color '#123E70' \
  --bottom-text $'Получите 1 монету из банка.\nВ ход любого игрока.' \
  --bottom-text-y-frac 0.82 \
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
  --caption "$caption" --caption-font fonts/Boingster-Regular.ttf --caption-font-size-frac 0.026 --caption-x-frac 0.58 --caption-y-frac 0.935 --caption-color '#D9E8F3'
