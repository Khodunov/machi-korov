#!/usr/bin/env bash
set -euo pipefail
.venv/bin/python skills/generate-card/scripts/landmark_compositor.py \
  --overlay buildings/zhd-stantsiya-04-polustanok.png \
  --title 'ЖД станция' \
  --rules $'Можете бросать два кубика\nвместо одного в свой ход.' \
  --cost 4 \
  --output-front cards/zhd-stantsiya-04-polustanok.png \
  --output-back card-backs/zhd-stantsiya-04-polustanok.png \
  --preview cards/zhd-stantsiya-04-polustanok-preview.png
