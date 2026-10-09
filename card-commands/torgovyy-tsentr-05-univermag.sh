#!/usr/bin/env bash
set -euo pipefail
.venv/bin/python skills/generate-card/scripts/landmark_compositor.py \
  --overlay buildings/torgovyy-tsentr-05-univermag.png \
  --title 'Торговый центр' \
  --rules $'Каждое ваше предприятие\nс символом {shop} или {restaurant}\nприносит на 1 монету больше.' \
  --cost 10 \
  --output-front cards/torgovyy-tsentr-05-univermag.png \
  --output-back card-backs/torgovyy-tsentr-05-univermag.png \
  --preview cards/torgovyy-tsentr-05-univermag-preview.png
