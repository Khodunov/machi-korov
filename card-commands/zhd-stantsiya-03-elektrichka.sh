#!/usr/bin/env bash
set -euo pipefail
.venv/bin/python skills/generate-card/scripts/landmark_compositor.py \
  --overlay buildings/zhd-stantsiya-03-elektrichka.png \
  --title 'ЖД станция' \
  --rules $'Можете бросать два кубика\nвместо одного в свой ход.' \
  --cost 4 \
  --output-front cards/zhd-stantsiya-03-elektrichka.png \
  --output-back card-backs/zhd-stantsiya-03-elektrichka.png \
  --preview cards/zhd-stantsiya-03-elektrichka-preview.png
