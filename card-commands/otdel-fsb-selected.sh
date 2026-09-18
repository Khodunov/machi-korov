set -euo pipefail

bash card-commands/otdel-fsb.sh
bash card-commands/otdel-fsb-01-seryy-korpus.sh
bash card-commands/otdel-fsb-02-kolonny.sh
bash card-commands/otdel-fsb-03-kirpich.sh
bash card-commands/otdel-fsb-04-sovetskiy.sh
.venv/bin/python skills/generate-card/scripts/build_otdel_fsb_preview.py
