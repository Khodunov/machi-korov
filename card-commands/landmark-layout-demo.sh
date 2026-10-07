#!/usr/bin/env bash
set -euo pipefail
# Layout specimen only. Existing artwork is a placeholder, not a new game card.
.venv/bin/python skills/generate-card/scripts/landmark_compositor.py \
  --overlay buildings/panelka.png \
  --title 'Достопримечательность' \
  --rules $'Здесь будет эффект\nдостопримечательности.\nДействует после постройки.' \
  --cost 22 \
  --output-front cards/landmark-layout-front.png \
  --output-back cards/landmark-layout-back.png \
  --preview cards/landmark-layout-preview.png \
  --output-construction-layer icons/landmark-construction-layer.png \
  --save-templates backgrounds
