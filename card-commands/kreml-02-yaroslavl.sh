#!/usr/bin/env bash
set -euo pipefail
.venv/bin/python skills/generate-card/scripts/landmark_compositor.py \
  --overlay buildings/kreml-02-yaroslavl.png \
  --title 'Кремль' --no-cost \
  --rules $'Если у вас нет монет,\nвозьмите одну монету из банка\nв свой ход перед строительством.' \
  --output-front cards/kreml-02-yaroslavl.png
