# Sanitized OpenSesame Visual-World Experiment

[![CI](https://github.com/viranovskaya/opensesame-visual-world-demo/actions/workflows/ci.yml/badge.svg)](https://github.com/viranovskaya/opensesame-visual-world-demo/actions/workflows/ci.yml)

A small, reproducible demonstration of an auditory two-alternative visual-world task. It shows trial randomisation, auditory cues, timed keyboard responses, accuracy scoring, timeout handling, and trial-level logging without releasing research data or third-party stimuli.

## What the task does

On every trial, the participant hears a brief cue and sees a target image and a distractor. Their task is to choose the side containing the target:

- `F` — left image
- `J` — right image
- response window — 2 seconds

The demo contains eight balanced, randomly ordered trials. Target position is randomised within each trial. The experiment records response, response time, timeout status, correct key, and accuracy.

## My contribution

I designed the experiment logic and rebuilt the task as a privacy-safe OpenSesame demo based on programming patterns from my MSc work. I wrote the deterministic asset and package builders, separated response scoring into testable Python functions, and validated the packaged experiment with automated responses.

## Repository contents

```text
assets/                 Generated geometric images and tone cues
docs/                   Method and privacy/provenance notes
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

Both build scripts are deterministic. Rebuilding replaces only generated demo assets and experiment packages.

## Validation

The packaged experiment was parsed and run headlessly with OpenSesame 3.3.10 using automated responses and dummy audio/video drivers. All eight trials completed and produced eight trial-level log rows. Automated repository tests additionally cover scoring, package contents, and common privacy leaks.

The test suite and deterministic rebuild check run automatically on every pull request.

## Relationship to the MSc project

This demo draws on programming patterns from my 2022 MSc project, *Chronotype and Time of Day Effects in Learning and Subjective Time Perception*. It is not the original experiment or a dataset; the scientific study and this software demo should be evaluated separately.

See [Methods](docs/methods.md) and [Privacy and provenance](docs/privacy_and_provenance.md) for the exact boundaries of the public artifact.

## License

Code and newly generated demo assets are released under the MIT License. No original participant records, consent forms, photographs, recordings, or third-party experimental stimuli are included.
