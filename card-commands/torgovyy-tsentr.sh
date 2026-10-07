#!/usr/bin/env bash
set -euo pipefail
.venv/bin/python skills/generate-card/scripts/landmark_compositor.py \
  --overlay buildings/torgovyy-tsentr.png \
  --title 'Торговый центр' \
  --rules $'Каждое ваше предприятие\nс символом «Торговая лавка»\nили «Бокал с вилкой»\nприносит на 1 монету больше.' \
  --cost 10 \
  --output-front cards/torgovyy-tsentr.png \
  --output-back card-backs/torgovyy-tsentr.png \
  --preview cards/torgovyy-tsentr-preview.png
