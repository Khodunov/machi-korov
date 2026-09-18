set -euo pipefail

bash card-commands/panelka.sh
bash card-commands/panelka-01-kover-v2.sh
bash card-commands/panelka-02-lebedi-v2.sh
bash card-commands/panelka-03-ogorod-v2.sh
bash card-commands/panelka-04-uteplenie-v2.sh
bash card-commands/panelka-05-kosmodrom-v2.sh
bash card-commands/panelka-06-balkony-v2.sh
bash card-commands/panelka-07-korabl-v2.sh
bash card-commands/panelka-08-sugrob-v2.sh
bash card-commands/panelka-09-mozaika-v2.sh
bash card-commands/panelka-10-tropinka-v4.sh
.venv/bin/python skills/generate-card/scripts/build_panelka_preview.py
