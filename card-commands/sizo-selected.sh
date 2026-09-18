set -euo pipefail

bash card-commands/sizo.sh
bash card-commands/sizo-01-avtozak.sh
bash card-commands/sizo-02-peredachi.sh
bash card-commands/sizo-03-kresty.sh
bash card-commands/sizo-04-matrosskaya-tishina.sh
.venv/bin/python skills/generate-card/scripts/build_sizo_preview.py
