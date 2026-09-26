
import pytest

from toolkit.converter import convert
from toolkit.errors import ConverterError


@pytest.mark.parametrize(
    ("value", "from_unit", "to_unit", "expected"),
    [
        (1000.0, "mm", "m", 1.0),
        (1.0, "kg", "g", 1000.0),
        (50.0, "  kg  ", "g  ", 50000.0),
        (-273.15, "c", "k", 0.0),
        (1.0, "CM", "m", 0.01),
        (100.0, "c", "k", 373.15),
        (1000.0, "G", "KG", 1.0),
        (0.0, "c", "f", 32.0),
        (212.0, "f", "c", 100.0),
        (32.0, "f", "k", 273.15),
    ],
)
def test_convert_positive(value: float, from_unit: str, to_unit: str, expected: float) -> None:
    assert convert(value, from_unit, to_unit) == pytest.approx(expected)

@pytest.mark.parametrize(
    ("value", "from_unit", "to_unit", "error_code"),
    [
        (1.0, "kg", "m", "different_group"),
        (5.0, "m", "c", "different_group"),
        (7.0, "kggg", "m", "unknown_unit"),
        (2.0, "c", "CcCc ", "unknown_unit"),
        (-300.0, "c", "k", "below_absolute_zero"),
    ],
)
def test_convert_negative(value: float, from_unit: str, to_unit: str, error_code: str) -> None:
    with pytest.raises(ConverterError) as exc_info:
        convert(value, from_unit, to_unit)
    assert exc_info.value.error_code == error_code
