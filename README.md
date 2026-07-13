# OpenSesame visual-world experiment

[![CI](https://github.com/viranovskaya/opensesame-visual-world-demo/actions/workflows/ci.yml/badge.svg)](https://github.com/viranovskaya/opensesame-visual-world-demo/actions/workflows/ci.yml)

This is a small auditory visual-world task that can be opened and run in OpenSesame. I rebuilt it from experimental-programming patterns I used during my MSc, using new geometric images and tone cues instead of the original research materials.

## What the task does

On every trial, the participant hears a brief cue and sees a target image and a distractor. Their task is to choose the side containing the target:

- `F` — left image
- `J` — right image
- response window — 2 seconds

The task contains eight balanced trials in random order. The target side is also randomised. For every trial, the experiment records the response, response time, timeout, correct key, and accuracy.

## My contribution

I wrote the task logic, the scripts that create the stimuli and OpenSesame package, and the response-scoring functions. I also added automated responses so that I could check whether a complete run produces the expected eight log rows.

## Repository contents

```text
assets/                 Generated geometric images and tone cues
docs/                   Method and notes on the source materials
experiment/             Trial manifest and runnable OpenSesame package
scripts/                Deterministic asset and experiment builders
src/visual_world/       Testable response-scoring logic
tests/                   Logic, package, and repository-safety tests
```

## Run the experiment

1. Install [OpenSesame](https://osdoc.cogsci.nl/).
2. Open `experiment/visual_world_demo.osexp`.
3. Run in windowed mode first and check that audio output and the `F`/`J` keys work.

The package is generated for the OpenSesame 3.x script format. A plain-text version is also provided as `experiment/visual_world_demo.opensesame` for inspection and version control.

## Rebuild from source

```bash
python -m pip install -e '.[dev]'
python scripts/generate_demo_assets.py
python scripts/build_experiment.py
pytest
```

Both scripts use the same trial inputs. Rebuilding replaces the generated stimuli and experiment packages. PNG encoding can differ across operating systems, although the task content stays the same.

## Validation

I ran the packaged experiment with OpenSesame 3.3.10 using automated responses and dummy audio/video drivers. All eight trials completed and produced eight log rows. The tests also check response scoring, package contents, and accidental inclusion of private files.

Every pull request rebuilds the task and runs the same checks.

## Relationship to the MSc project

The code is related to my 2022 MSc project, *Chronotype and Time of Day Effects in Learning and Subjective Time Perception*, but this is not the original experiment and it contains no study data. The trial set, images, and sounds were made for this repository.

See [Methods](docs/methods.md) for the task sequence and [Source materials and privacy](docs/privacy_and_provenance.md) for what is and is not included.

## License

The code and generated demo stimuli are released under the MIT License.
