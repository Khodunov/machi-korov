#!/usr/bin/env bash
set -euo pipefail
.venv/bin/python skills/generate-card/scripts/landmark_compositor.py \
  --overlay buildings/airport-01-sheremetyevo.png \
  --title 'Аэропорт' \
  --rules $'Если в свой ход вы\nничего не построили,\nполучите 10 монет\nиз банка.' \
  --cost 30 \
  --output-front cards/airport-01-sheremetyevo.png \
  --output-back card-backs/airport-01-sheremetyevo.png \
  --preview cards/airport-01-sheremetyevo-preview.png
