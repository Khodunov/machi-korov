#!/usr/bin/env bash
set -euo pipefail
.venv/bin/python skills/generate-card/scripts/landmark_compositor.py \
  --overlay buildings/torgovyy-tsentr-03-kupol-v2.png \
  --title 'Торговый центр' \
  --rules $'Каждое ваше предприятие\nс символом {shop} или {restaurant}\nприносит на 1 монету больше.' \
  --cost 10 \
  --output-front cards/torgovyy-tsentr-03-kupol-v2.png \
  --output-back card-backs/torgovyy-tsentr-03-kupol-v2.png \
  --preview cards/torgovyy-tsentr-03-kupol-v2-preview.png
