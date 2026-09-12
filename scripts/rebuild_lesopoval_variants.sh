#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
.venv/bin/python scripts/remove_lesopoval_background.py buildings/originals/lesopoval-01-dvuruchnaya-pila.png buildings/lesopoval-01-dvuruchnaya-pila.png
bash card-commands/lesopoval-01-dvuruchnaya-pila.sh
.venv/bin/python scripts/remove_lesopoval_background.py buildings/originals/lesopoval-03-trelevochnik.png buildings/lesopoval-03-trelevochnik.png
bash card-commands/lesopoval-03-trelevochnik.sh
.venv/bin/python scripts/remove_lesopoval_background.py buildings/originals/lesopoval-05-uzkokoleyka.png buildings/lesopoval-05-uzkokoleyka.png --background-seed 630 300 --background-seed 420 330 --background-seed 1120 490 --background-seed 820 610
bash card-commands/lesopoval-05-uzkokoleyka.sh
