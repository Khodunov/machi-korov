#!/usr/bin/env bash
set -euo pipefail
.venv/bin/python skills/generate-card/scripts/landmark_compositor.py \
  --overlay buildings/mfc-05-panelka.png \
  --title 'МФЦ' \
  --rules $'Если на двух кубиках\nвыпал дубль, сделайте\nещё один ход.\nВ свой ход.' \
  --cost 16 \
  --output-front cards/mfc-05-panelka.png \
  --output-back card-backs/mfc-05-panelka.png \
  --preview cards/mfc-05-panelka-preview.png
