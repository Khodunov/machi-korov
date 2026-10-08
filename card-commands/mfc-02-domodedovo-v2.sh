#!/usr/bin/env bash
set -euo pipefail
.venv/bin/python skills/generate-card/scripts/landmark_compositor.py \
  --overlay buildings/mfc-02-domodedovo-v2.png \
  --title 'МФЦ' \
  --rules $'Если на двух кубиках\nвыпал дубль, сделайте\nещё один ход.\nВ свой ход.' \
  --cost 16 \
  --output-front cards/mfc-02-domodedovo-v2.png \
  --output-back card-backs/mfc-02-domodedovo-v2.png \
  --preview cards/mfc-02-domodedovo-v2-preview.png
