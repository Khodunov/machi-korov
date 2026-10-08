#!/usr/bin/env bash
set -euo pipefail
.venv/bin/python skills/generate-card/scripts/landmark_compositor.py \
  --overlay buildings/gostelekanal-03-shabolovka.png \
  --title 'Гостелеканал' \
  --rules $'Один раз можете\nперебросить кубики\nв свой ход.' \
  --cost 22 \
  --output-front cards/gostelekanal-03-shabolovka.png \
  --output-back card-backs/gostelekanal-03-shabolovka.png \
  --preview cards/gostelekanal-03-shabolovka-preview.png
