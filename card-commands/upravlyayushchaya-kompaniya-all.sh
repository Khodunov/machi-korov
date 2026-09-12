set -euo pipefail

for variant in 1-final 2 3 4 5-revised 6; do
  bash "card-commands/upravlyayushchaya-kompaniya-v${variant}.sh"
done
.venv/bin/python skills/generate-card/scripts/build_upravlyayushchaya_preview.py
