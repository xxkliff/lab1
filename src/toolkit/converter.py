
import math

from toolkit.constants import GROUPS, TEMPERATURE_GROUP
from toolkit.errors import ConverterError


def _validate(value: float, from_unit: str, to_unit: str) -> dict:
    if not math.isfinite(value):
        raise ConverterError(message="значение не является числом или бесконечно.", error_code="not_a_number")

    group_from = _find_group(from_unit)
    group_to = _find_group(to_unit)

    if group_from != group_to:
        raise ConverterError(message=f"единицы измерения '{from_unit}' и '{to_unit}' находятся в разных группах и "
                                     f"несовместимы с друг другом.",
                             error_code="different_group")

    if (from_unit == 'c' and value < -273.15) or (from_unit == 'f' and value < -459.67) or (from_unit == 'k' and value < 0):
        raise ConverterError(message="температура не может быть ниже абсолютного нуля",
                             error_code="below_absolute_zero")

    if group_from != TEMPERATURE_GROUP and value < 0:
        raise ConverterError(message="значение для данной группы не может быть отрицательным.",
                             error_code="negative_value")

    return group_from

def _find_group(unit: str) -> dict:
    groups = [group for group in GROUPS if unit in group]

    if len(groups) > 1:
        raise RuntimeError("Ошибка в исходном составлении групп")
    if len(groups) == 0:
        raise ConverterError(message=f"неизвестная единица '{unit}'", error_code="unknown_unit")

    return groups[0]


def convert(value: float, from_unit: str, to_unit: str) -> float:
    from_unit, to_unit = from_unit.lower().strip(), to_unit.lower().strip()
    group = _validate(value, from_unit, to_unit)

    if from_unit in ('c', 'f', 'k'):
        to_kelvin = TEMPERATURE_GROUP[from_unit][0](value)
        new_scale = TEMPERATURE_GROUP[to_unit][1](to_kelvin)

        return new_scale

    return value * group[from_unit] / group[to_unit]
