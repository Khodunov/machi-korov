caption=$(.venv/bin/python -c 'import json; print(next(c for c in json.load(open("cards-config.json"))["cards"] if c["slug"] == "setevoy-magazin")["caption"])')

.venv/bin/python skills/generate-card/scripts/card_compositor.py \
  --template backgrounds/green.png \
  --overlay buildings/setevoy-magazin-magnit.png \
  --title-icon icons/shop-stall.png \
  --shadow \
  --output cards/setevoy-magazin-magnit.png \
  --x-frac 0.50 \
  --y-frac 0.51 \
  --scale 0.73 \
  --coin-number 2 \
  --activation-number 4 \
  --title 'Сетевой магазин' \
  --title-color '#17361A' \
  --bottom-text $'Получите 3 монеты из банка.\nВ свой ход.' \
  --bottom-text-y-frac 0.82 \
  --bottom-text-spacing-px 6 \
  --title-font fonts/Boingster-Regular.ttf \
  --title-font-size-frac 0.078 \
  --title-icon-scale 1.88 \
  --title-icon-gap-px 12 \
  --title-icon-y-offset-px -10 \
  --bottom-text-font fonts/CCUltimatum-Bold.ttf \
  --bottom-text-font-size-frac 0.05 \
  --activation-font fonts/CCUltimatum-Bold.ttf \
  --activation-font-size-frac 0.118 \
  --coin-font fonts/Boingster-Regular.ttf \
  --caption "$caption" --caption-font fonts/Boingster-Regular.ttf --caption-font-size-frac 0.026 --caption-x-frac 0.58 --caption-y-frac 0.935 --caption-color "#D8E5C8"
