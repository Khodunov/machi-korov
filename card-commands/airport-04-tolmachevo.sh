#!/usr/bin/env bash
set -euo pipefail
.venv/bin/python skills/generate-card/scripts/landmark_compositor.py \
  --overlay buildings/airport-04-tolmachevo.png \
  --title 'Аэропорт' \
  --rules $'Если в свой ход вы\nничего не построили,\nполучите 10 монет\nиз банка.' \
  --cost 30 \
  --output-front cards/airport-04-tolmachevo.png \
  --output-back card-backs/airport-04-tolmachevo.png \
  --preview cards/airport-04-tolmachevo-preview.png
