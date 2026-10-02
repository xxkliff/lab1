import math
from typing import Any

from toolkit.constants import GROUPS, TEMPERATURE_GROUP
from toolkit.errors import ConverterError


def _find_group(unit: str) -> dict[str, Any]:
    """
    Находит группу, к которой относится единица измерения

    Группы описаны в constants.py

    :param unit: единица измерения в нижнем регистре и без пробелов
    :return: словарь группы, в которой есть эта единица
    :raises RuntimeError: ошибка программиста, единица измерения одновременно находится в нескольких группах
    :raises ConverterError: выкидывается, когда единица не находится ни в одной группе (неизвестная)
    """
    groups = [group for group in GROUPS if unit in group]

    if len(groups) > 1:
        raise RuntimeError("Ошибка в исходном составлении групп")
    if len(groups) == 0:
        raise ConverterError(message=f"неизвестная единица '{unit}'", error_code="unknown_unit")

    return groups[0]


def _validate(value: float, from_unit: str, to_unit: str) -> dict[str, float]:
    """
    Проверяет, что выражение корректно: значение конечно, единицы известны и из одной группы, температура не ниже
    абсолютного нуля, длина и масса не отрицательны, значение и пара единиц допустимы для конвертации.

    :param value: исходное значение
    :param from_unit: единица в нижнем регистре и без пробелов
    :param to_unit: новая единица в нижнем регистре и без пробелов
    :return: группа двух единиц
    :raises ConverterError: выкидывает при любых возможных ошибках с определённым error_code
    """
    if not math.isfinite(value):
        raise ConverterError(message="значение не является числом или бесконечно.", error_code="not_a_number")

    group_from = _find_group(from_unit)
    group_to = _find_group(to_unit)

    if group_from is not group_to:
        raise ConverterError(message=f"единицы измерения '{from_unit}' и '{to_unit}' находятся в разных группах и "
                                     f"несовместимы друг с другом.",
                             error_code="different_group")

    if group_from is TEMPERATURE_GROUP and TEMPERATURE_GROUP[from_unit][0](value) < 0:
        raise ConverterError(message="температура не может быть ниже абсолютного нуля",
                             error_code="below_absolute_zero")

    if group_from is not TEMPERATURE_GROUP and value < 0:
        raise ConverterError(message="значение для данной группы не может быть отрицательным.",
                             error_code="negative_value")

    return group_from


def convert(value: float, from_unit: str, to_unit: str) -> float:
    """
    Переводит значение из одной единицы измерения в другую

    Регистр и пробелы вокруг единицы не учитываются.

    :param value: исходное значение
    :param from_unit: исходная единица
    :param to_unit: целевая единица
    :return: значение в целевой единице
    :raises ConverterError: ошибки из _validate
    """
    from_unit, to_unit = from_unit.lower().strip(), to_unit.lower().strip()
    group = _validate(value, from_unit, to_unit)

    if from_unit in TEMPERATURE_GROUP:
        to_kelvin = TEMPERATURE_GROUP[from_unit][0](value)
        new_scale = TEMPERATURE_GROUP[to_unit][1](to_kelvin)

        return float(new_scale)

    return float(value * group[from_unit] / group[to_unit])
