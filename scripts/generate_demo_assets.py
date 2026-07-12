#!/usr/bin/env python3
"""Generate original geometric images and synthesized auditory cues."""

from __future__ import annotations

import csv
import math
import struct
import wave
from pathlib import Path

from PIL import Image, ImageDraw


ROOT = Path(__file__).resolve().parents[1]
ASSET_DIR = ROOT / "assets"
MANIFEST = ROOT / "experiment" / "trials.csv"

TARGET_COLOURS = [
    "#2D6CDF",
    "#008F7A",
    "#7B61FF",
    "#D1495B",
    "#0077B6",
    "#6A994E",
    "#B56576",
    "#F77F00",
]
DISTRACTOR_COLOURS = [
    "#F4A261",
    "#E9C46A",
    "#90BE6D",
    "#F28482",
    "#84A59D",
    "#BC6C25",
    "#577590",
    "#CDB4DB",
]


def read_trials() -> list[dict[str, str]]:
    with MANIFEST.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def draw_stimulus(path: Path, colour: str, label: str, shape_index: int) -> None:
    image = Image.new("RGB", (420, 320), "#F7F7F5")
    draw = ImageDraw.Draw(image)
    draw.rounded_rectangle((8, 8, 411, 311), radius=24, outline="#30343F", width=5)
    box = (105, 55, 315, 245)
    if shape_index % 4 == 0:
        draw.ellipse(box, fill=colour, outline="#20242C", width=5)
    elif shape_index % 4 == 1:
        draw.rounded_rectangle(box, radius=28, fill=colour, outline="#20242C", width=5)
    elif shape_index % 4 == 2:
        draw.polygon([(210, 42), (328, 242), (92, 242)], fill=colour, outline="#20242C")
    else:
        draw.regular_polygon((210, 150, 112), n_sides=6, rotation=30, fill=colour, outline="#20242C")
    draw.text((24, 278), label, fill="#20242C")
    image.save(path, optimize=True)


def write_tone(path: Path, frequency: float, duration: float = 0.45) -> None:
    sample_rate = 44_100
    frames = int(sample_rate * duration)
    fade_frames = int(sample_rate * 0.03)
    samples: list[bytes] = []
    for index in range(frames):
        envelope = min(1.0, index / fade_frames, (frames - index - 1) / fade_frames)
        value = 0.25 * envelope * math.sin(2.0 * math.pi * frequency * index / sample_rate)
        samples.append(struct.pack("<h", int(value * 32_767)))
    with wave.open(str(path), "wb") as handle:
        handle.setnchannels(1)
        handle.setsampwidth(2)
        handle.setframerate(sample_rate)
        handle.writeframes(b"".join(samples))


def main() -> None:
    ASSET_DIR.mkdir(parents=True, exist_ok=True)
    for index, trial in enumerate(read_trials()):
        draw_stimulus(
            ASSET_DIR / trial["target_image"],
            TARGET_COLOURS[index],
            f"Target {index + 1}",
            index,
        )
        draw_stimulus(
            ASSET_DIR / trial["distractor_image"],
            DISTRACTOR_COLOURS[index],
            f"Alternative {index + 1}",
            index + 2,
        )
        write_tone(ASSET_DIR / trial["cue"], 330.0 + 45.0 * index)
    print(f"Generated {len(read_trials()) * 3} demo assets in {ASSET_DIR}")


if __name__ == "__main__":
    main()

