set -euo pipefail

.venv/bin/python skills/generate-card/scripts/remove_light_background.py \
  buildings/upravlyayushchaya-kompaniya-v1-final-source.png \
  buildings/upravlyayushchaya-kompaniya-v1-final.png \
  --background-seed 600 110

.venv/bin/python skills/generate-card/scripts/card_compositor.py \
  --template backgrounds/green.png \
  --overlay buildings/upravlyayushchaya-kompaniya-v1-final.png \
  --title-icon icons/house-in-gear.png \
  --shadow \
  --output cards/upravlyayushchaya-kompaniya-v1-final.png \
  --x-frac 0.50 \
  --y-frac 0.50 \
  --scale 0.65 \
  --coin-number 2 \
  --activation-number '11–12' \
  --title 'Управляющая компания' \
  --title-color '#17361A' \
  --bottom-text $'Получите по 2 монеты за каждую\nсвою «Панельку» и «Новостройку».' \
  --bottom-text-y-frac 0.825 \
  --bottom-text-spacing-px 5 \
  --title-font fonts/Boingster-Regular.ttf \
  --title-font-size-frac 0.052 \
  --title-icon-scale 1.88 \
  --title-icon-gap-px 10 \
  --title-icon-y-offset-px -8 \
  --bottom-text-font fonts/CCUltimatum-Bold.ttf \
  --bottom-text-font-size-frac 0.0377 \
  --activation-font fonts/CCUltimatum-Bold.ttf \
  --activation-font-size-frac 0.118 \
  --coin-font fonts/Boingster-Regular.ttf
