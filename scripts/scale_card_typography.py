#!/usr/bin/env python3
"""Scale title/header typography across card-commands/*.sh."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

MULTIPLIERS = {
    "title-font-size-frac": 1.42,
    "title-icon-scale": 1.25,
    "activation-font-size-frac": 1.18,
    "bottom-text-font-size-frac": 1.11,
}

PATTERN = re.compile(
    r"--(" + "|".join(re.escape(key) for key in MULTIPLIERS) + r")\s+([0-9.]+)"
)


def format_value(value: float) -> str:
    text = f"{value:.4f}".rstrip("0").rstrip(".")
    return text or "0"


def scale_file(path: Path) -> bool:
    text = path.read_text()

    def replace(match: re.Match[str]) -> str:
        key = match.group(1)
        scaled = float(match.group(2)) * MULTIPLIERS[key]
        return f"--{key} {format_value(scaled)}"

    updated = PATTERN.sub(replace, text)
    if updated != text:
        path.write_text(updated)
        return True
    return False


def main() -> None:
    changed = 0
    for path in sorted((ROOT / "card-commands").glob("*.sh")):
        if scale_file(path):
            changed += 1
    print(f"Updated typography in {changed} card command(s).")


if __name__ == "__main__":
    main()
