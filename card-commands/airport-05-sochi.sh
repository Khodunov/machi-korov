#!/usr/bin/env bash
set -euo pipefail
.venv/bin/python skills/generate-card/scripts/landmark_compositor.py \
  --overlay buildings/airport-05-sochi.png \
  --title 'Аэропорт' \
  --rules $'Если в свой ход вы\nничего не построили,\nполучите 10 монет из банка.' \
  --cost 30 \
  --output-front cards/airport-05-sochi.png \
  --output-back card-backs/airport-05-sochi.png \
  --preview cards/airport-05-sochi-preview.png
