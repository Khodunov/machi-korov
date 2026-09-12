set -euo pipefail

.venv/bin/python skills/generate-card/scripts/remove_light_background.py \
  buildings/upravlyayushchaya-kompaniya-v6-source.png \
  buildings/upravlyayushchaya-kompaniya-v6.png \
  --background-seed 1235 670 \
  --background-seed 1250 672 \
  --background-seed 1234 682 \
  --background-seed 1258 683 \
  --background-seed 125 699 \
  --background-seed 1252 706 \
  --background-seed 1268 706 \
  --background-seed 95 711 \
  --background-seed 98 717 \
  --background-seed 79 718 \
  --background-seed 80 745 \
  --background-seed 88 751

.venv/bin/python skills/generate-card/scripts/card_compositor.py \
  --template backgrounds/green.png \
  --overlay buildings/upravlyayushchaya-kompaniya-v6.png \
  --title-icon icons/house.png \
  --shadow \
  --output cards/upravlyayushchaya-kompaniya-v6.png \
  --x-frac 0.50 \
  --y-frac 0.50 \
  --scale 0.67 \
  --coin-number 2 \
  --activation-number '11–12' \
  --title 'Управляющая компания' \
  --title-color '#17361A' \
  --bottom-text $'Получи 2 монеты за каждую карту\nпанельки и новостройки' \
  --bottom-text-y-frac 0.825 \
  --bottom-text-spacing-px 5 \
  --title-font fonts/Boingster-Regular.ttf \
  --title-font-size-frac 0.043 \
  --title-icon-scale 1.45 \
  --title-icon-y-offset-px -8 \
  --bottom-text-font fonts/CCUltimatum-Bold.ttf \
  --bottom-text-font-size-frac 0.034 \
  --activation-font fonts/CCUltimatum-Bold.ttf \
  --activation-font-size-frac 0.086 \
  --coin-font fonts/Boingster-Regular.ttf \
  --caption 'Каждая точка под контролем' \
  --caption-font fonts/Boingster-Regular.ttf \
  --caption-font-size-frac 0.030 \
  --caption-x-frac 0.58 \
  --caption-y-frac 0.915 \
  --caption-color '#D8E5C8'
