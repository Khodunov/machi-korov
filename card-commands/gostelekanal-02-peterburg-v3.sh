#!/usr/bin/env bash
set -euo pipefail
.venv/bin/python skills/generate-card/scripts/landmark_compositor.py \
  --overlay buildings/gostelekanal-02-peterburg-v3.png \
  --title 'Гостелеканал' \
  --rules $'Один раз можете\nперебросить кубики\nв свой ход.' \
  --cost 22 \
  --output-front cards/gostelekanal-02-peterburg-v3.png \
  --output-back card-backs/gostelekanal-02-peterburg-v3.png \
  --preview cards/gostelekanal-02-peterburg-v3-preview.png
