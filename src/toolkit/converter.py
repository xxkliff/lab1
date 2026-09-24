
import math

from src.constants import LENGTH_GROUP, GROUPS, TEMPERATURE_GROUP
from toolkit.errors import ConverterError

def _validate(value: float, from_unit: str, to_unit: str) -> bool:
    if not math.isfinite(value):
        raise ConverterError(message="Значение не является числом либо бесконечно", error_code="not_a_number")

    if _find_group(from_unit) != _find_group(to_unit):
        raise ConverterError(message=f"Единицы {from_unit} и {to_unit} находятся в разных группах",
                             error_code="different_group")

    if (from_unit == 'c' and value < -273.15) or (from_unit == 'f' and value < -459.67) or (from_unit == 'k' and value < 0):
        raise ConverterError(message="Температура не может быть ниже абсолютного нуля",
                             error_code="below_absolute_zero")

    return True

def _find_group(unit: str) -> dict:
    groups = [group for group in GROUPS if unit in group]

    if len(groups) > 1:
        raise RuntimeError("Ошибка в исходном составлении групп")
    if len(groups) == 0:
        raise ConverterError(message=f"Единица {unit} не существует", error_code="unknown_unit")

    return groups[0]


def convert(value: float, from_unit: str, to_unit: str) -> float:
    from_unit, to_unit = from_unit.lower(), to_unit.lower()
    _validate(value, from_unit, to_unit)

    if from_unit in ('c', 'f', 'k'):
        to_kelvin = TEMPERATURE_GROUP[from_unit][0](value)
        new_scale = TEMPERATURE_GROUP[to_unit][1](to_kelvin)

        return new_scale

    return value * LENGTH_GROUP[from_unit] / LENGTH_GROUP[to_unit]

print(convert(-273.15, from_unit='c', to_unit='k'))
