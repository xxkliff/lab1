from datetime import datetime
from pathlib import Path

import pytest

from toolkit.errors import HistoryError
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
    ("content", "error_code"),
    [
        ("[[[", "json_decode_error"),
        ("не json", "json_decode_error"),
        ("{}", "json_history_format"),
    ]
)
def test_invalid_json(tmp_path: Path, content: str, error_code: str) -> None:
    path = tmp_path / "history.json"

    path.write_text(content, encoding="utf-8")

    with pytest.raises(HistoryError) as exc:
        load_history(path)
    assert exc.value.error_code == error_code
    assert path.read_text(encoding="utf-8") == content


def test_load_history(tmp_path: Path) -> None:
    path = tmp_path / "missing.json"

    assert load_history(path) == []
    assert not path.exists()


@pytest.mark.parametrize(
    "entries",
    [
        (("2+2", 4.0), ("1+1", 2.0)),
        (("calc 1 + 3 * 4", 13.0), ("calc 2 / 2", 1.0), ("convert 1000m -> 1 km", 1.0))

    ],
)
def test_multiple_entry(tmp_path: Path, entries: tuple[tuple[str, float], ...]) -> None:
    path = tmp_path / "history.json"

    for expression, result in entries:
        add_entry(path, expression, result)

    history = load_history(path)

    expected_history = [{"expression": expression, "result": result} for expression, result in entries]
    saved_history = [{"expression": entry["expression"], "result": entry["result"]} for entry in history]

    assert expected_history == saved_history
    assert all(datetime.strptime(item["time"], "%Y-%m-%d %H:%M:%S") for item in history)  # noqa: DTZ007
