set -euo pipefail

bash card-commands/autoservice.sh
bash card-commands/autoservice-01-petrovich.sh
bash card-commands/autoservice-02-patsany.sh
bash card-commands/autoservice-03-pervyy-sneg.sh
bash card-commands/autoservice-05-malyarka.sh
bash card-commands/autoservice-07-gazel.sh
.venv/bin/python skills/generate-card/scripts/build_autoservice_preview.py
