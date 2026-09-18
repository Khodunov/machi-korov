set -euo pipefail

bash card-commands/garazhnyy-kooperativ.sh
bash card-commands/garazhnyy-kooperativ-batina-volga.sh
bash card-commands/garazhnyy-kooperativ-kartoshka-v2.sh
bash card-commands/garazhnyy-kooperativ-rakushka-v2.sh
bash card-commands/garazhnyy-kooperativ-rybalka-v2.sh
bash card-commands/garazhnyy-kooperativ-seychas-zavedem-v2.sh
.venv/bin/python skills/generate-card/scripts/build_garazh_preview.py
