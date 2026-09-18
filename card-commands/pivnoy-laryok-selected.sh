set -euo pipefail

bash card-commands/pivnoy-laryok.sh
bash card-commands/pivnoy-laryok-01-zhvachka-v3.sh
bash card-commands/pivnoy-laryok-02-domoy-v3.sh
bash card-commands/pivnoy-laryok-03-kozyrek-v3.sh
bash card-commands/pivnoy-laryok-04-tropa-v3.sh
bash card-commands/pivnoy-laryok-05-futbol-v3.sh
bash card-commands/pivnoy-laryok-06-ostrovok-v3.sh
bash card-commands/pivnoy-laryok-07-bez-sdachi-v3.sh
bash card-commands/pivnoy-laryok-08-minutka-v3.sh
bash card-commands/pivnoy-laryok-09-kot-v3.sh
bash card-commands/pivnoy-laryok-10-novyy-god-v3.sh
.venv/bin/python skills/generate-card/scripts/build_pivnoy_laryok_preview.py
