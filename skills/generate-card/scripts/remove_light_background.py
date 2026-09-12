#!/usr/bin/env python3
"""Remove only edge-connected near-white background from generated card art."""

import argparse
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw


def remove_background(source: Path, output: Path, seeds: list[tuple[int, int]]) -> None:
    image = Image.open(source).convert("RGB")
    rgb = np.asarray(image).astype(np.float32)
    low, high = rgb.min(axis=2), rgb.max(axis=2)
    # Paper notices and white interior details remain opaque unless connected
    # to the outer canvas. No global white-color replacement is performed.
    candidate = ((low >= 235) & ((high - low) <= 22)).astype(np.uint8)
    mask = Image.fromarray(candidate).copy()
    w, h = image.size
    for x, y in [(x, y) for x in range(w) for y in (0, h - 1)] + [
        (x, y) for y in range(h) for x in (0, w - 1)
    ]:
        if mask.getpixel((x, y)) == 1:
            ImageDraw.floodfill(mask, (x, y), 2)
    for seed in seeds:
        if mask.getpixel(seed) == 1:
            ImageDraw.floodfill(mask, seed, 2)
        elif mask.getpixel(seed) != 2:
            raise ValueError(f"Background seed {seed} is not on near-white background.")
    exterior = np.asarray(mask) == 2
    alpha = np.where(exterior, 0.0, 1.0)
    # Remove the pale antialias fringe only immediately along the cut edge.
    padded = np.pad(exterior, 1, constant_values=True)
    adjacent = np.zeros_like(exterior)
    for dy in range(3):
        for dx in range(3):
            adjacent |= padded[dy : dy + h, dx : dx + w]
    fringe = adjacent & ~exterior & (low > 190) & ((high - low) < 30)
    alpha[fringe] = np.clip((255 - low[fringe]) / 65, 0, 1)
    safe_alpha = np.maximum(alpha[..., None], 1 / 255)
    unmatted = np.clip((rgb - 255 * (1 - safe_alpha)) / safe_alpha, 0, 255)
    rgba = np.dstack((unmatted.astype(np.uint8), (alpha * 255).astype(np.uint8)))
    result = Image.fromarray(rgba)
    bbox = result.getchannel("A").getbbox()
    if bbox is None:
        raise ValueError("Background removal erased the entire image.")
    if not exterior.any():
        raise ValueError("No near-white background connected to the canvas edges.")
    output.parent.mkdir(parents=True, exist_ok=True)
    result.save(output)
    print(f"{output}: removed {exterior.mean():.1%} background; subject bounds {bbox}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--background-seed", type=int, nargs=2, action="append", default=[])
    args = parser.parse_args()
    remove_background(args.source, args.output, [tuple(seed) for seed in args.background_seed])
