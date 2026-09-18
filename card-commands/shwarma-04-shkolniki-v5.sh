set -euo pipefail

caption=$(.venv/bin/python -c 'import json; print(next(c for c in json.load(open("cards-config.json"))["cards"] if c["slug"] == "shwarma")["caption"])')

.venv/bin/python skills/generate-card/scripts/card_compositor.py \
  --template backgrounds/red.png \
  --overlay buildings/shwarma-04-shkolniki-v5.png \
  --title-icon icons/glass-and-fork.png \
  --shadow \
  --output cards/shwarma-04-shkolniki-v5.png \
  --x-frac 0.50 \
  --y-frac 0.52 \
  --scale 0.64 \
  --coin-number 2 \
  --activation-number 3 \
  --title 'Шавуха' \
  --title-color '#58100E' \
  --bottom-text $'Получите 1 монету у игрока,\nбросившего кубики.\nВ ход другого игрока.' \
  --bottom-text-y-frac 0.81 \
  --bottom-text-spacing-px 6 \
  --title-font fonts/Boingster-Regular.ttf \
  --title-font-size-frac 0.078 \
  --title-icon-scale 1.88 \
  --title-icon-gap-px 12 \
  --title-icon-y-offset-px -10 \
  --bottom-text-font fonts/CCUltimatum-Bold.ttf \
  --bottom-text-font-size-frac 0.0389 \
  --activation-font fonts/CCUltimatum-Bold.ttf \
  --activation-font-size-frac 0.118 \
  --coin-font fonts/Boingster-Regular.ttf \
  --caption "$caption" --caption-font fonts/Boingster-Regular.ttf --caption-font-size-frac 0.026 --caption-x-frac 0.58 --caption-y-frac 0.935 --caption-color '#EDD3CD'
