set -euo pipefail

bash card-commands/karaoke-klub.sh
bash card-commands/karaoke-klub-01-podval-90h.sh
bash card-commands/karaoke-klub-06-tsokol.sh
bash card-commands/karaoke-klub-07-byvshee-kafe.sh
bash card-commands/karaoke-klub-09-kirpich.sh
bash card-commands/karaoke-klub-10-pridorozhny.sh
.venv/bin/python skills/generate-card/scripts/build_karaoke_preview.py
