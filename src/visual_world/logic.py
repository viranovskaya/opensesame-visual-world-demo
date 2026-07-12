"""Response mapping and scoring independent of the OpenSesame runtime."""

from __future__ import annotations


POSITION_TO_KEY = {
    "centerleft": "f",
    "centerright": "j",
}


def correct_key(target_position: str) -> str:
    """Return the expected response key for a horizontal target position."""
    try:
        return POSITION_TO_KEY[target_position]
    except KeyError as exc:
        allowed = ", ".join(POSITION_TO_KEY)
        raise ValueError(f"Unknown target position {target_position!r}; expected {allowed}") from exc


def score_response(target_position: str, response: str | None) -> bool:
    """Return whether a response selects the side containing the target."""
    if response is None:
        return False
    return response.lower() == correct_key(target_position)


def accuracy_percent(correct: int, total: int) -> float:
    """Return accuracy as a percentage rounded to one decimal place."""
    if correct < 0:
        raise ValueError("correct must be non-negative")
    if total < 0:
        raise ValueError("total must be non-negative")
    if correct > total:
        raise ValueError("correct cannot exceed total")
    if total == 0:
        return 0.0
    return round(100.0 * correct / total, 1)

