set -euo pipefail

bash card-commands/novostroyka.sh
bash card-commands/novostroyka-01-murino-stena.sh
bash card-commands/novostroyka-02-devyatkino-kolodets.sh
bash card-commands/novostroyka-03-pik-bashni.sh
bash card-commands/novostroyka-04-samolet-grebenka.sh
bash card-commands/novostroyka-05-megadom-stupeni.sh
.venv/bin/python skills/generate-card/scripts/build_novostroyka_preview.py
