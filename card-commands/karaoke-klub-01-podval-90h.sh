caption=$(.venv/bin/python -c 'import json; print(next(c for c in json.load(open("cards-config.json"))["cards"] if c["slug"] == "karaoke-klub")["caption"])')

.venv/bin/python skills/generate-card/scripts/card_compositor.py \
  --template backgrounds/red.png \
  --overlay buildings/karaoke-klub-01-podval-90h-building.png \
  --title-icon icons/glass-and-fork.png \
  --shadow \
  --output cards/karaoke-klub-01-podval-90h.png \
  --x-frac 0.50 --y-frac 0.49 --scale 0.65 \
  --coin-number 3 --activation-number '9–10' \
  --title 'Караоке-клуб' --title-color '#58100E' \
  --bottom-text $'Получите 2 монеты у игрока,\nбросившего кубики.\nВ ход другого игрока.' \
  --bottom-text-y-frac 0.84 --bottom-text-spacing-px 6 \
  --title-font fonts/Boingster-Regular.ttf --title-font-size-frac 0.078 \
  --title-icon-scale 1.88 --title-icon-y-offset-px -10 \
  --bottom-text-font fonts/CCUltimatum-Bold.ttf --bottom-text-font-size-frac 0.0366 \
  --activation-font fonts/CCUltimatum-Bold.ttf --activation-font-size-frac 0.118 \
  --coin-font fonts/Boingster-Regular.ttf \
  --caption "$caption" \
  --caption-font fonts/Boingster-Regular.ttf \
  --caption-font-size-frac 0.026 \
  --caption-x-frac 0.58 \
  --caption-y-frac 0.935 \
  --caption-color "#F3D7C9"
