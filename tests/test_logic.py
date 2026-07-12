import pytest

from visual_world import accuracy_percent, correct_key, score_response


def test_correct_key_maps_left_and_right() -> None:
    assert correct_key("centerleft") == "f"
    assert correct_key("centerright") == "j"


def test_correct_key_rejects_unknown_position() -> None:
    with pytest.raises(ValueError, match="Unknown target position"):
        correct_key("centre")


@pytest.mark.parametrize(
    ("position", "response", "expected"),
    [
        ("centerleft", "f", True),
        ("centerleft", "F", True),
        ("centerleft", "j", False),
        ("centerright", "j", True),
        ("centerright", None, False),
    ],
)
def test_score_response(position: str, response: str | None, expected: bool) -> None:
    assert score_response(position, response) is expected


def test_accuracy_percent() -> None:
    assert accuracy_percent(0, 0) == 0.0
    assert accuracy_percent(7, 8) == 87.5


@pytest.mark.parametrize(("correct", "total"), [(-1, 1), (2, 1), (0, -1)])
def test_accuracy_rejects_impossible_counts(correct: int, total: int) -> None:
    with pytest.raises(ValueError):
        accuracy_percent(correct, total)

