#!/usr/bin/env bash
set -euo pipefail
.venv/bin/python skills/generate-card/scripts/landmark_compositor.py \
  --overlay buildings/airport-02-pulkovo.png \
  --title 'Аэропорт' \
  --rules $'Если в свой ход вы\nничего не построили,\nполучите 10 монет\nиз банка.' \
  --cost 30 \
  --output-front cards/airport-02-pulkovo.png \
  --output-back card-backs/airport-02-pulkovo.png \
  --preview cards/airport-02-pulkovo-preview.png
