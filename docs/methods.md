# Demonstration method

## Purpose

This task demonstrates the implementation of an auditory two-alternative forced-choice visual-world paradigm in OpenSesame. It is intentionally compact and uses synthetic stimuli so that the execution logic can be inspected without exposing research materials.

## Trial sequence

Each of the eight trials follows the same sequence:

1. blank screen — 1,000 ms;
2. fixation cross and auditory cue — up to 1,000 ms;
3. fixation interval — 500 ms;
4. target and distractor display — 2,000 ms response window;
5. timeout feedback when no accepted key is recorded;
6. trial-level logging.

Trial order is randomised. The target and distractor positions are shuffled horizontally within every trial. The response mapping is `F` for left and `J` for right.

## Recorded variables

The OpenSesame logger records the standard runtime variables and the following task variables:

- target and distractor filenames;
- auditory cue filename;
- target position;
- response key;
- response time in milliseconds;
- whether the response timed out;
- expected key;
- trial correctness;
- cumulative number correct;
- cumulative accuracy.

## Deliberate differences from the research workflow

The public demo uses eight generated trials rather than the full research stimulus set. It uses neutral geometric drawings and pure-tone cues, and the response keys were changed to a conventional left/right `F`/`J` mapping. These changes mean that behavioral results from this demo are not comparable with the original study.

## Validation scope

Automated tests cover response mapping, scoring, accuracy calculation, package contents, and common privacy leaks. They do not replace timing validation on the intended computer, monitor, keyboard, headphones, or OpenSesame version.

