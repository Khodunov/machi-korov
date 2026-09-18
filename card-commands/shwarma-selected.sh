set -euo pipefail

bash card-commands/shwarma.sh
bash card-commands/shwarma-01-tsokol-v5.sh
bash card-commands/shwarma-02-marshrutka-v5.sh
bash card-commands/shwarma-03-zima-v5.sh
bash card-commands/shwarma-04-shkolniki-v5.sh
bash card-commands/shwarma-05-stolik-v5.sh
.venv/bin/python skills/generate-card/scripts/build_shwarma_preview.py
