#!/usr/bin/env bash
set -euo pipefail
.venv/bin/python skills/generate-card/scripts/landmark_compositor.py \
  --overlay buildings/gostelekanal-05-ekaterinburg.png \
  --title 'Гостелеканал' \
  --rules $'Один раз можете\nперебросить кубики\nв свой ход.' \
  --cost 22 \
  --output-front cards/gostelekanal-05-ekaterinburg.png \
  --output-back card-backs/gostelekanal-05-ekaterinburg.png \
  --preview cards/gostelekanal-05-ekaterinburg-preview.png
