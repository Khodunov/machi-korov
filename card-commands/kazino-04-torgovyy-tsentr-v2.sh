set -euo pipefail

.venv/bin/python skills/generate-card/scripts/card_compositor.py \
  --template backgrounds/red.png \
  --overlay buildings/kazino-04-torgovyy-tsentr-v2.png \
  --title-icon icons/gambling-chip.png \
  --title-icon-scale 1.55 --title-icon-gap-px 10 --title-icon-y-offset-px -5 \
  --shadow \
  --output cards/kazino-04-torgovyy-tsentr-v2.png \
  --x-frac 0.50 --y-frac 0.50 --scale 0.70 \
  --coin-number 3 --activation-number 7 \
  --title 'Казино' --title-color '#58100E' \
  --bottom-text $'Попавший игрок бросает 2 кубика.\nДубль — вы платите ему 2 монеты.\nИначе он платит вам 3 монеты.' \
  --bottom-text-y-frac 0.825 --bottom-text-spacing-px 8 \
  --title-font fonts/Boingster-Regular.ttf --title-font-size-frac 0.078 \
  --bottom-text-font fonts/CCUltimatum-Bold.ttf --bottom-text-font-size-frac 0.034 \
  --activation-font fonts/CCUltimatum-Bold.ttf --activation-font-size-frac 0.118 \
  --coin-font fonts/Boingster-Regular.ttf
