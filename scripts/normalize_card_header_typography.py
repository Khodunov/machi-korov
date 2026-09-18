#!/usr/bin/env python3
"""Set one canonical title/header typography across card-commands/*.sh."""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from card_layout import (  # noqa: E402
    ACTIVATION_FONT_SIZE_FRAC,
    TITLE_FONT_SIZE_FRAC,
    TITLE_ICON_GAP_PX,
    TITLE_ICON_SCALE,
    TITLE_ICON_Y_OFFSET_PX,
)

REPLACE_KEYS = {
    "title-font-size-frac": f"{TITLE_FONT_SIZE_FRAC:g}",
    "activation-font-size-frac": f"{ACTIVATION_FONT_SIZE_FRAC:g}",
    "title-icon-scale": f"{TITLE_ICON_SCALE:g}",
    "title-icon-gap-px": str(TITLE_ICON_GAP_PX),
    "title-icon-y-offset-px": str(TITLE_ICON_Y_OFFSET_PX),
}

KEY_PATTERN = re.compile(
    r"--(" + "|".join(re.escape(key) for key in REPLACE_KEYS) + r")\s+[^\s\\]+"
)


def normalize_file(path: Path) -> bool:
    text = path.read_text()
    if "--title-font-size-frac" not in text:
        return False

    has_title_icon = "--title-icon " in text
    updated = KEY_PATTERN.sub(
        lambda match: f"--{match.group(1)} {REPLACE_KEYS[match.group(1)]}",
        text,
    )

    if has_title_icon:
        if "--title-icon-scale" not in updated:
            updated = updated.replace(
                f"  --title-font-size-frac {REPLACE_KEYS['title-font-size-frac']} \\",
                "  --title-font-size-frac "
                f"{REPLACE_KEYS['title-font-size-frac']} \\\n"
                f"  --title-icon-scale {REPLACE_KEYS['title-icon-scale']} \\",
                1,
            )
        if "--title-icon-gap-px" not in updated:
            updated = updated.replace(
                f"  --title-icon-scale {REPLACE_KEYS['title-icon-scale']} \\",
                "  --title-icon-scale "
                f"{REPLACE_KEYS['title-icon-scale']} \\\n"
                f"  --title-icon-gap-px {REPLACE_KEYS['title-icon-gap-px']} \\",
                1,
            )
        if "--title-icon-y-offset-px" not in updated:
            anchor = f"  --title-icon-gap-px {REPLACE_KEYS['title-icon-gap-px']} \\"
            if anchor in updated:
                updated = updated.replace(
                    anchor,
                    anchor
                    + "\n"
                    + f"  --title-icon-y-offset-px {REPLACE_KEYS['title-icon-y-offset-px']} \\",
                    1,
                )
            else:
                updated = updated.replace(
                    f"  --title-icon-scale {REPLACE_KEYS['title-icon-scale']} \\",
                    "  --title-icon-scale "
                    f"{REPLACE_KEYS['title-icon-scale']} \\\n"
                    f"  --title-icon-y-offset-px {REPLACE_KEYS['title-icon-y-offset-px']} \\",
                    1,
                )

    if updated != text:
        path.write_text(updated)
        return True
    return False


def main() -> None:
    changed = sum(
        1 for path in sorted((ROOT / "card-commands").glob("*.sh")) if normalize_file(path)
    )
    print(f"Normalized header typography in {changed} card command(s).")


if __name__ == "__main__":
    main()
