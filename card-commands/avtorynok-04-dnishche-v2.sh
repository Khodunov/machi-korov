set -euo pipefail

caption=$(.venv/bin/python -c 'import json; print(next(c for c in json.load(open("cards-config.json"))["cards"] if c["slug"] == "avtorynok")["caption"])')

.venv/bin/python skills/generate-card/scripts/card_compositor.py --template backgrounds/green.png --overlay buildings/avtorynok-04-dnishche-v2.png --output cards/avtorynok-04-dnishche-v2.png --title-icon icons/soviet-car.png --shadow --x-frac 0.50 --y-frac 0.47 --scale 0.78 --coin-number 5 --activation-number 7 --title 'Авторынок' --title-color '#17361A' --bottom-text 'Получите по 3 монеты
за каждый свой гараж.
В свой ход.' --footer-rise-frac 0.09 --bottom-text-y-frac 0.785 --bottom-text-spacing-px 8 --title-font fonts/Boingster-Regular.ttf --title-font-size-frac 0.078 --title-icon-size-frac 0.119140625 --title-icon-gap-px 12 --title-icon-y-offset-px -10 --bottom-text-font fonts/CCUltimatum-Bold.ttf --bottom-text-font-size-frac 0.05 --activation-font fonts/CCUltimatum-Bold.ttf --activation-font-size-frac 0.118 --coin-font fonts/Boingster-Regular.ttf \
  --caption "$caption" --caption-font fonts/Boingster-Regular.ttf --caption-font-size-frac 0.026 --caption-x-frac 0.58 --caption-y-frac 0.935 --caption-color '#D8E5C8'
