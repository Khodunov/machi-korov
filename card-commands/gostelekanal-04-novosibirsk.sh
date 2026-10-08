#!/usr/bin/env bash
set -euo pipefail
.venv/bin/python skills/generate-card/scripts/landmark_compositor.py \
  --overlay buildings/gostelekanal-04-novosibirsk.png \
  --title 'Гостелеканал' \
  --rules $'Один раз можете\nперебросить кубики\nв свой ход.' \
  --cost 22 \
  --output-front cards/gostelekanal-04-novosibirsk.png \
  --output-back card-backs/gostelekanal-04-novosibirsk.png \
  --preview cards/gostelekanal-04-novosibirsk-preview.png
