# Task method

## Purpose

This is an auditory two-alternative visual-world task implemented in OpenSesame. I kept it to eight trials and used generated stimuli so that the complete task can be run without the original research materials.

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

## Differences from the MSc task

This version uses eight generated trials instead of the original stimulus set. It uses geometric drawings and pure-tone cues, and the response keys are `F` and `J`. Therefore behavioural results from this task cannot be compared with the MSc study.

## Validation scope

The automated tests check response mapping, scoring, accuracy, package contents, and accidental inclusion of private files. Timing still has to be checked on the computer, monitor, keyboard, headphones, and OpenSesame version used for an actual experiment.
