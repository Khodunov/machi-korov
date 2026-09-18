caption=$(.venv/bin/python -c 'import json; print(next(c for c in json.load(open("cards-config.json"))["cards"] if c["slug"] == "hram")["caption"])')

.venv/bin/python skills/generate-card/scripts/card_compositor.py \
  --template backgrounds/purple.png \
  --overlay buildings/hram-03-svechi-kartoy-v2.png \
  --title-icon icons/purple-tower.png \
  --shadow \
  --output cards/hram-03-svechi-kartoy-v2.png \
  --x-frac 0.5 \
  --y-frac 0.53 \
  --scale 0.7207 \
  --coin-number 6 \
  --activation-number 6 \
  --title 'Храм' \
  --title-color '#3E1F59' \
  --bottom-text $'Получите по 2 монеты\nу каждого соперника.\nВ свой ход.' \
  --bottom-text-y-frac 0.82 \
  --bottom-text-spacing-px 6 \
  --title-font fonts/Boingster-Regular.ttf \
  --title-font-size-frac 0.078 \
  --title-icon-scale 1.88 \
  --title-icon-gap-px 12 \
  --title-icon-y-offset-px -10 \
  --bottom-text-font fonts/CCUltimatum-Bold.ttf \
  --bottom-text-font-size-frac 0.0477 \
  --activation-font fonts/CCUltimatum-Bold.ttf \
  --activation-font-size-frac 0.118 \
  --coin-font fonts/Boingster-Regular.ttf \
  --caption "$caption" --caption-font fonts/Boingster-Regular.ttf --caption-font-size-frac 0.026 --caption-x-frac 0.58 --caption-y-frac 0.935 --caption-color "#E3D5EF"
