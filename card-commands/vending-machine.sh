set -euo pipefail

caption=$(.venv/bin/python -c 'import json; print(next(c for c in json.load(open("cards-config.json"))["cards"] if c["slug"] == "vending-machine")["caption"])')

.venv/bin/python skills/generate-card/scripts/card_compositor.py \
  --template backgrounds/red.png \
  --overlay buildings/vending-machine.png \
  --title-icon icons/service-triad.png \
  --shadow \
  --output cards/vending-machine.png \
  --x-frac 0.50 \
  --y-frac 0.49 \
  --scale 0.40 \
  --coin-number 2 \
  --activation-number '4' \
  --title 'Вендинговый автомат' \
  --title-color '#58100E' \
  --bottom-text $'Сет из вендингового автомата,\nавтомойки и автосервиса.\n1 сет приносит 2.\n2 сета приносит 3.' \
  --bottom-text-y-frac 0.84 \
  --bottom-text-spacing-px 6 \
  --title-font fonts/Boingster-Regular.ttf \
  --title-font-size-frac 0.068 \
  --title-icon-scale 1.55 \
  --title-icon-gap-px 10 \
  --title-icon-y-offset-px -4 \
  --bottom-text-font fonts/CCUltimatum-Bold.ttf \
  --bottom-text-font-size-frac 0.035 \
  --activation-font fonts/CCUltimatum-Bold.ttf \
  --activation-font-size-frac 0.118 \
  --coin-font fonts/Boingster-Regular.ttf \
  --caption "$caption" --caption-font fonts/Boingster-Regular.ttf --caption-font-size-frac 0.026 --caption-x-frac 0.58 --caption-y-frac 0.935 --caption-color '#EDD3CD'
