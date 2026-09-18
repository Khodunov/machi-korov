set -euo pipefail

bash card-commands/eksport-v-kitay.sh
bash card-commands/eksport-v-kitay-01-pogruzchik-v2.sh
bash card-commands/eksport-v-kitay-02-konteynerovoz-v2.sh
bash card-commands/eksport-v-kitay-03-tanker-v2.sh
bash card-commands/eksport-v-kitay-04-gruzoviki-v2.sh
bash card-commands/eksport-v-kitay-05-sostavy-v2.sh
.venv/bin/python skills/generate-card/scripts/build_eksport_v_kitay_preview.py
