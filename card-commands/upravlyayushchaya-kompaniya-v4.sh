set -euo pipefail

.venv/bin/python skills/generate-card/scripts/remove_light_background.py \
  buildings/upravlyayushchaya-kompaniya-v4-source.png \
  buildings/upravlyayushchaya-kompaniya-v4.png

.venv/bin/python skills/generate-card/scripts/card_compositor.py \
  --template backgrounds/green.png \
  --overlay buildings/upravlyayushchaya-kompaniya-v4.png \
  --title-icon icons/house.png \
  --shadow \
  --output cards/upravlyayushchaya-kompaniya-v4.png \
  --x-frac 0.50 \
  --y-frac 0.50 \
  --scale 0.55 \
  --coin-number 2 \
  --activation-number '11–12' \
  --title 'Управляющая компания' \
  --title-color '#17361A' \
  --bottom-text $'Получи 2 монеты за каждую карту\nпанельки и новостройки' \
  --bottom-text-y-frac 0.825 \
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
  --caption 'Каждая точка под контролем' \
  --caption-font fonts/Boingster-Regular.ttf \
  --caption-font-size-frac 0.030 \
  --caption-x-frac 0.58 \
  --caption-y-frac 0.915 \
  --caption-color '#D8E5C8'
