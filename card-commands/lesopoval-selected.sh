set -euo pipefail

bash card-commands/lesopoval.sh
bash card-commands/lesopoval-01-dvuruchnaya-pila-v2.sh
bash card-commands/lesopoval-02-pilorama-v2.sh
bash card-commands/lesopoval-03-trelevochnik-v2.sh
bash card-commands/lesopoval-04-stalinskiy-lespromkhoz-v2.sh
bash card-commands/lesopoval-05-uzkokoleyka-v2.sh
.venv/bin/python skills/generate-card/scripts/build_lesopoval_preview.py
