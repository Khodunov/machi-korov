#!/usr/bin/env bash
set -euo pipefail
.venv/bin/python skills/generate-card/scripts/landmark_compositor.py \
  --overlay buildings/torgovyy-tsentr-03-kupol.png \
  --title 'Торговый центр' \
  --rules $'Каждое ваше предприятие\nс символом «Торговая лавка»\nили «Бокал с вилкой»\nприносит на 1 монету больше.' \
  --cost 10 \
  --output-front cards/torgovyy-tsentr-03-kupol.png \
  --output-back card-backs/torgovyy-tsentr-03-kupol.png \
  --preview cards/torgovyy-tsentr-03-kupol-preview.png
