from datetime import datetime
from pathlib import Path

import pytest

from toolkit.history import add_entry, load_history


@pytest.mark.parametrize(
    ("expression", "result"),
    [
        ("2+2", 4.0),
        ("calc 1+5", 6.0),
        ("convert 1000 m -> 1 km ", 1.0)
    ],
)
def test_add_entry(tmp_path: Path, expression: str, result: float) -> None:
    path = tmp_path / "history.json"

    add_entry(path, expression, result)
    history = load_history(path)

    assert history[0]["expression"] == expression
    assert history[0]["result"] == result
    assert len(history) == 1


@pytest.mark.parametrize(
    "entries",
    [
        (("2+2", 4.0), ("1+1", 2.0)),
        (("calc 1 + 3 * 4", 13.0), ("calc 2 / 2", 1.0), ("convert 1000m -> 1 km", 1.0))

    ],
)
def test_multiple_entry(tmp_path: Path, entries: tuple[tuple[str, float], ...]) -> None:
    path = tmp_path / "history.json"
    
    for entry in entries:
        add_entry(path, entry[0], entry[1])

    history = load_history(path)

    expected_history = [{"expression": expression, "result": result} for expression, result in entries]
    saved_history = [{"expression": entry["expression"], "result": entry["result"]} for entry in history]

    assert expected_history == saved_history
    assert all(datetime.strptime(item["time"], "%Y-%m-%d %H:%M:%S") for item in history)  # noqa: DTZ007
