"""Preview the centralized caption with its original styling, without replacing cards."""
import json
from pathlib import Path
import shlex
import subprocess

root = Path(__file__).resolve().parents[1]
config = json.loads((root / "cards-config.json").read_text())
card = next(c for c in config["cards"] if c["slug"] == "upravlyayushchaya-kompaniya")
for variant in ("1-final", "2", "3", "4", "5-revised", "6"):
    slug = f"upravlyayushchaya-kompaniya-v{variant}"
    source = (root / f"card-commands/{slug}.sh").read_text()
    command = source[source.index(".venv/bin/python skills/generate-card/scripts/card_compositor.py"):].strip()
    options = [
        "--output", f"cards/{slug}-with-caption.png",
        "--caption", card["caption"],
        "--caption-font", "fonts/Boingster-Regular.ttf",
        "--caption-font-size-frac", "0.030",
        "--caption-x-frac", "0.58", "--caption-y-frac", "0.915",
        "--caption-color", "#D8E5C8",
    ]
    subprocess.run(["bash", "-c", command + " " + shlex.join(options)], cwd=root, check=True)
subprocess.run([
    ".venv/bin/python", "skills/generate-card/scripts/build_upravlyayushchaya_preview.py",
    "--suffix=-with-caption",
], cwd=root, check=True)
