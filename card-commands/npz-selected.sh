set -euo pipefail

bash card-commands/npz.sh
bash card-commands/npz-bashneft.sh
bash card-commands/npz-gazprom-neft.sh
bash card-commands/npz-rosneft.sh
bash card-commands/npz-surgutneftegaz.sh
bash card-commands/npz-tatneft.sh
.venv/bin/python skills/generate-card/scripts/build_npz_preview.py
