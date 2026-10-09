#!/usr/bin/env bash
set -euo pipefail
.venv/bin/python skills/generate-card/scripts/landmark_compositor.py \
  --overlay buildings/mfc-05-falyonki-v3.png \
  --title 'МФЦ' \
  --rules $'Если на двух кубиках выпал дубль,\nсделайте ещё один ход.\nВ свой ход.' \
  --cost 16 \
  --output-front cards/mfc-05-falyonki-v3.png \
  --output-back card-backs/mfc-05-falyonki-v3.png \
  --preview cards/mfc-05-falyonki-v3-preview.png
