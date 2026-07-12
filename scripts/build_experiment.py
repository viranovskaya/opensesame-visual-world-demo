#!/usr/bin/env python3
"""Build the plain OpenSesame script and the portable .osexp package."""

from __future__ import annotations

import csv
import gzip
import io
import tarfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ASSET_DIR = ROOT / "assets"
EXPERIMENT_DIR = ROOT / "experiment"
MANIFEST = EXPERIMENT_DIR / "trials.csv"
PLAIN_SCRIPT = EXPERIMENT_DIR / "visual_world_demo.opensesame"
PACKAGE = EXPERIMENT_DIR / "visual_world_demo.osexp"


def read_trials() -> list[dict[str, str]]:
    with MANIFEST.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def trial_cycles(trials: list[dict[str, str]]) -> str:
    lines: list[str] = []
    for index, trial in enumerate(trials):
        lines.extend(
            [
                f'\tsetcycle {index} trial_id "{trial["trial_id"]}"',
                f'\tsetcycle {index} target_image "{trial["target_image"]}"',
                f'\tsetcycle {index} distractor_image "{trial["distractor_image"]}"',
                f'\tsetcycle {index} cue "{trial["cue"]}"',
                f'\tsetcycle {index} target_position "centerleft"',
                f'\tsetcycle {index} distractor_position "centerright"',
            ]
        )
    return "\n".join(lines)


def build_script(trials: list[dict[str, str]]) -> str:
    cycles = trial_cycles(trials)
    return f'''---
API: 2.1
OpenSesame: 3.3.9
Platform: posix
---
set width 1024
set height 768
set uniform_coordinates yes
set foreground white
set background black
set description "Sanitized auditory visual-world demonstration"
set title "Visual World Demo"
set subject_nr 0
set response ""
set response_time -1
set response_timeout 0
set correct_key ""
set correct 0
set total_correct 0
set total_trials 0
set accuracy_percent 0.0
set summary_text "Accuracy will be shown here"
set start experiment_sequence

define sequence experiment_sequence
\tset flush_keyboard yes
\tset description "Main experiment sequence"
\trun initialize always
\trun instructions always
\trun trial_loop always
\trun calculate_summary always
\trun summary always

define inline_script initialize
\tset description "Initialize aggregate variables"
\t___run__
\tvar.total_correct = 0
\tvar.total_trials = 0
\tvar.accuracy_percent = 0.0
\t__end__
\tset _prepare ""

define sketchpad instructions
\tset duration keypress
\tset description "Participant instructions"
\tdraw textline center=1 color=white font_family=sans font_size=28 html=yes text="Choose the image that matches the sound." x=0 y=-120 z_index=0
\tdraw textline center=1 color=white font_family=sans font_size=24 html=yes text="F = left     J = right" x=0 y=-30 z_index=0
\tdraw textline center=1 color=white font_family=sans font_size=20 html=yes text="Respond within 2 seconds. Press any key to begin." x=0 y=70 z_index=0

define loop trial_loop
\tset break_if_on_first yes
\tset repeat 1
\tset order random
\tset description "Eight randomized demo trials"
\tset cycles {len(trials)}
\tset continuous no
\tset source_file ""
\tset source table
{cycles}
\tshuffle_horiz target_position distractor_position
\trun trial_sequence

define sequence trial_sequence
\tset flush_keyboard yes
\tset description "Single trial"
\trun blank always
\trun fixation_onset always
\trun fixation_and_sound always
\trun post_sound_fixation always
\trun image_display always
\trun collect_response always
\trun timeout_feedback "[response_timeout] = 1"
\trun trial_logger always

define sketchpad blank
\tset duration 1000
\tset description "Inter-trial blank"

define sketchpad fixation_onset
\tset duration 0
\tset description "Display fixation before the cue"
\tdraw fixdot color=white style=default x=0 y=0 z_index=0

define sampler fixation_and_sound
\tset description "Auditory cue"
\tset duration sound
\tset fade_in 0
\tset pan 0
\tset pitch 1
\tset sample "[cue]"
\tset stop_after 1000
\tset volume 1

define sketchpad post_sound_fixation
\tset duration 500
\tset description "Fixation interval"
\tdraw fixdot color=white style=default x=0 y=0 z_index=0

define sketchpad image_display
\tset duration 0
\tset description "Target and distractor display"
\tdraw image center=1 file="[target_image]" scale=0.65 x="[=-256 if 'left' in var.target_position else 256]" y=0 z_index=0
\tdraw image center=1 file="[distractor_image]" scale=0.65 x="[=-256 if 'left' in var.distractor_position else 256]" y=0 z_index=0

define inline_script collect_response
\tset description "Timed response and professional scoring variables"
\t___run__
\tkeyboard = Keyboard(keylist=[u'f', u'j'], timeout=2000)
\tstart_time = clock.time()
\tresponse, end_time = keyboard.get_key()
\tvar.response = response
\tvar.response_time = end_time - start_time
\tvar.response_timeout = int(response is None)
\tvar.correct_key = 'f' if var.target_position == 'centerleft' else 'j'
\tvar.correct = int(response == var.correct_key)
\tvar.total_trials += 1
\tvar.total_correct += var.correct
\tvar.accuracy_percent = round(100.0 * var.total_correct / var.total_trials, 1)
\t__end__
\tset _prepare ""

define sketchpad timeout_feedback
\tset duration 500
\tset description "Shown only after timeout"
\tdraw textline center=1 color=white font_family=sans font_size=28 html=yes text="Please respond faster" x=0 y=0 z_index=0

define logger trial_logger
\tset description "Trial-level output"
\tset auto_log no
\tlog trial_id
\tlog target_image
\tlog distractor_image
\tlog cue
\tlog target_position
\tlog response
\tlog response_time
\tlog response_timeout
\tlog correct_key
\tlog correct
\tlog total_correct
\tlog total_trials
\tlog accuracy_percent

define inline_script calculate_summary
\tset description "Ensure summary is available"
\tset _prepare ""
\tset _run "var.summary_text = 'Accuracy: {{:.1f}}% ({{}}/{{}})'.format(var.accuracy_percent, var.total_correct, var.total_trials)"

define sketchpad summary
\tset duration keypress
\tset description "End screen"
\tdraw textline center=1 color=white font_family=sans font_size=30 html=yes text="Demo complete" x=0 y=-60 z_index=0
\tdraw textline center=1 color=white font_family=sans font_size=24 html=yes text="[summary_text]" x=0 y=10 z_index=0
\tdraw textline center=1 color=white font_family=sans font_size=18 html=yes text="Press any key to exit" x=0 y=80 z_index=0
'''


def add_bytes(archive: tarfile.TarFile, name: str, data: bytes) -> None:
    info = tarfile.TarInfo(name=name)
    info.size = len(data)
    info.mtime = 0
    archive.addfile(info, io.BytesIO(data))


def main() -> None:
    trials = read_trials()
    script = build_script(trials)
    PLAIN_SCRIPT.write_text(script, encoding="utf-8")

    required_assets = {
        trial[field]
        for trial in trials
        for field in ("target_image", "distractor_image", "cue")
    }
    missing = sorted(name for name in required_assets if not (ASSET_DIR / name).exists())
    if missing:
        raise FileNotFoundError(f"Missing generated assets: {', '.join(missing)}")

    with PACKAGE.open("wb") as raw_package:
        with gzip.GzipFile(filename="", mode="wb", fileobj=raw_package, mtime=0) as compressed:
            with tarfile.open(fileobj=compressed, mode="w", format=tarfile.GNU_FORMAT) as archive:
                add_bytes(archive, "script.opensesame", script.encode("utf-8"))
                for name in sorted(required_assets):
                    add_bytes(archive, f"pool/{name}", (ASSET_DIR / name).read_bytes())

    print(f"Built {PLAIN_SCRIPT.name} and {PACKAGE.name} with {len(trials)} trials")


if __name__ == "__main__":
    main()
