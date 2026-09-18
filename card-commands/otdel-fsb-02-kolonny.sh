set -euo pipefail

caption=$(.venv/bin/python -c 'import json; print(next(c for c in json.load(open("cards-config.json"))["cards"] if c["slug"] == "otdel-fsb")["caption"])')

.venv/bin/python skills/generate-card/scripts/card_compositor.py \
  --template backgrounds/purple.png \
  --overlay buildings/otdel-fsb-02-kolonny.png \
  --title-icon icons/purple-tower.png \
  --shadow \
  --output cards/otdel-fsb-02-kolonny.png \
  --x-frac 0.50 \
  --y-frac 0.50 \
  --scale 0.78 \
  --coin-number 8 \
  --activation-number 6 \
  --title 'Отдел ФСБ' \
  --title-color '#3E1F59' \
  --bottom-text $'Можете обменять одно своё\nпредприятие на чужое.\nФиолетовые карты не участвуют.\nВ свой ход.' \
  --bottom-text-y-frac 0.83 \
  --bottom-text-spacing-px 5 \
  --title-font fonts/Boingster-Regular.ttf \
  --title-font-size-frac 0.078 \
  --title-icon-scale 1.88 \
  --title-icon-gap-px 12 \
  --title-icon-y-offset-px -10 \
  --bottom-text-font fonts/CCUltimatum-Bold.ttf \
  --bottom-text-font-size-frac 0.0377 \
  --activation-font fonts/CCUltimatum-Bold.ttf \
  --activation-font-size-frac 0.118 \
  --coin-font fonts/Boingster-Regular.ttf \
  --caption "$caption" --caption-font fonts/Boingster-Regular.ttf --caption-font-size-frac 0.026 --caption-x-frac 0.58 --caption-y-frac 0.935 --caption-color "#E3D5EF"
