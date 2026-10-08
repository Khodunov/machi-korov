#!/usr/bin/env bash
set -euo pipefail
.venv/bin/python skills/generate-card/scripts/landmark_compositor.py \
  --overlay buildings/gostelekanal-01-ostankino.png \
  --title 'Гостелеканал' \
  --rules $'Один раз можете\nперебросить кубики\nв свой ход.' \
  --cost 22 \
  --output-front cards/gostelekanal-01-ostankino.png \
  --output-back card-backs/gostelekanal-01-ostankino.png \
  --preview cards/gostelekanal-01-ostankino-preview.png
