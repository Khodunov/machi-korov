set -euo pipefail

caption=$(.venv/bin/python -c 'import json; print(next(c for c in json.load(open("cards-config.json"))["cards"] if c["slug"] == "autoservice")["caption"])')

.venv/bin/python skills/generate-card/scripts/card_compositor.py \
  --template backgrounds/blue.png \
  --overlay buildings/autoservice-05-malyarka.png \
  --title-icon icons/soviet-car.png \
  --shadow \
  --output cards/autoservice-05-malyarka.png \
  --x-frac 0.50 \
  --y-frac 0.465 \
  --scale 0.68 \
  --coin-number 2 \
  --activation-number '8' \
  --title 'Автосервис' \
  --title-color '#123E70' \
  --bottom-text $'Сет из вендингового автомата,\nавтомойки и автосервиса.\n1 сет приносит 2.\n2 сета приносит 3' \
  --footer-rise-frac 0.09 \
  --bottom-text-y-frac 0.785 \
  --bottom-text-spacing-px 6 \
  --title-font fonts/Boingster-Regular.ttf \
  --title-font-size-frac 0.078 \
  --title-icon-size-frac 0.119140625 \
  --title-icon-gap-px 12 \
  --title-icon-y-offset-px -10 \
  --bottom-text-font fonts/CCUltimatum-Bold.ttf \
  --bottom-text-font-size-frac 0.045 \
  --activation-font fonts/CCUltimatum-Bold.ttf \
  --activation-font-size-frac 0.118 \
  --coin-font fonts/Boingster-Regular.ttf \
  --caption "$caption" --caption-font fonts/Boingster-Regular.ttf --caption-font-size-frac 0.026 --caption-x-frac 0.50 --caption-y-frac 0.935 --caption-color "#D9E8F3"
