
import pytest

from toolkit.calculator import evaluate
from toolkit.errors import ValidationError


@pytest.mark.parametrize(
    ("expression", "expected"),
    [
        ("2+3*4", 14),
        ("10/4", 2.5),
        ("2*-3", -6),
        ("1+-2", -1),
        ("1 + 2", 3),
        ("5 - 8",  -3),
        ("  2 +   3  ", 5),
        ("1.5 * 2", 3),
        ("+5- 2", 3),
        ("2 + 3 * 4 - 6 / 2", 11),
        ("7 // 2", 3),
        ("7 % 3", 1),
    ],
)
def test_evaluate_positive(expression: str, expected: float) -> None:
    assert evaluate(expression) == pytest.approx(expected)


@pytest.mark.parametrize(
    ("expression", "error_code"),
    [
        ("", "empty_expression"),
        ("2+a", "invalid_number"),
        ("2*/3", "unexpected_operator"),
        ("2+", "missing_operand"),
        ("1/0", "division_by_zero"),
        ("5//0", "division_by_zero"),
        ("10%0", "division_by_zero"),
        ("2 3", "missing_operator"),
        ("2 3.5", "missing_operator"),
    ],
)
def test_evaluate_negative(expression: str, error_code: str) -> None:
    with pytest.raises(ValidationError) as exc_info:
        evaluate(expression)
    assert exc_info.value.error_code == error_code
