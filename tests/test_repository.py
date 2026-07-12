from __future__ import annotations

import csv
import tarfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_manifest_has_eight_synthetic_trials() -> None:
    with (ROOT / "experiment" / "trials.csv").open(newline="", encoding="utf-8") as handle:
        trials = list(csv.DictReader(handle))
    assert len(trials) == 8
    assert len({trial["target_image"] for trial in trials}) == 8
    assert len({trial["distractor_image"] for trial in trials}) == 8
    assert len({trial["cue"] for trial in trials}) == 8


def test_opensesame_package_contains_only_script_and_generated_assets() -> None:
    package = ROOT / "experiment" / "visual_world_demo.osexp"
    with tarfile.open(package, "r:gz") as archive:
        names = archive.getnames()
    assert names[0] == "script.opensesame"
    assert len(names) == 25
    assert all(name == "script.opensesame" or name.startswith("pool/") for name in names)


def test_multiline_inline_python_uses_opensesame_block_syntax() -> None:
    script = (ROOT / "experiment" / "visual_world_demo.opensesame").read_text(encoding="utf-8")
    assert script.count("\t___run__") == 2
    assert script.count("\t__end__") == 2
    assert "set _run \"keyboard" not in script
    assert "x=\"[=-256 if 'left' in var.target_position else 256]\"" in script


def test_text_files_do_not_contain_common_private_artifacts() -> None:
    forbidden = [
        "Email",
        "/Users/",
        "total_fucking",
        "@gmail",
        "participant_code",
    ]
    paths = [
        *ROOT.glob("*.md"),
        *ROOT.glob("*.toml"),
        *ROOT.glob("docs/*.md"),
        *ROOT.glob("scripts/*.py"),
        *ROOT.glob("src/**/*.py"),
        ROOT / "experiment" / "visual_world_demo.opensesame",
    ]
    combined = "\n".join(path.read_text(encoding="utf-8") for path in paths)
    for marker in forbidden:
        assert marker not in combined
