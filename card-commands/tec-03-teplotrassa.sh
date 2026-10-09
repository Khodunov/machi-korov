#!/usr/bin/env bash
set -euo pipefail
.venv/bin/python skills/generate-card/scripts/landmark_compositor.py \
  --overlay buildings/tec-03-teplotrassa.png \
  --title 'ТЭЦ' \
  --rules $'В свой ход можете\nприбавить 1 или вычесть 1\nиз результата броска кубика.' \
  --cost 26 \
  --output-front cards/tec-03-teplotrassa.png \
  --output-back card-backs/tec-03-teplotrassa.png \
  --preview cards/tec-03-teplotrassa-preview.png
