import argparse
import sys
from pathlib import Path

from toolkit.calculator import evaluate
from toolkit.constants import DEFAULT_HISTORY_PATH
from toolkit.converter import convert
from toolkit.errors import HistoryError, ToolkitError
from toolkit.history import add_entry


def _convert_func(args: argparse.Namespace) -> tuple[str, float]:
    """
    Переводит значение из аргументов команды convert и печатает результат в stdout.

    :return: результат для истории
    """
    result = convert(args.value, args.from_unit, args.to_unit)
    expression = f"{args.value:.10g} {args.from_unit} -> {result:.10g} {args.to_unit}"
    print(expression)

    return "convert " + expression, result


def _calculate_func(args: argparse.Namespace) -> tuple[str, float]:
    """
    Вычисляет выражение из аргументов команды calc и печатает результат в stdout.

    :return: результат для истории
    """
    result = evaluate(args.expression)
    print(f"{result:.10g}")

    return "calc " + args.expression, result


def main(argv: list[str] | None = None, history_path: Path | None = DEFAULT_HISTORY_PATH) -> int:
    """
    Точка входа CLI, разбирает команду на аргументы и вызывает convert и evaluate

    Результат идет в stdout, а ошибки ядра (ToolkitError) в stderr. Все остальные ошибки, связанные с
    разработчиком, обрабатываются стандартными ошибками Python

    :param history_path: путь к json файлу с историей
    :param argv: аргументы команды. Если None - берутся из командной строки
    :return: 0 при успехе, 2 при ошибке
    """
    parser = argparse.ArgumentParser(
        prog="toolkit",
        description="Набор утилит: калькулятор и конвертер единиц")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # python -m toolkit calc "expression"
    calc_parser = subparsers.add_parser("calc", help='вычислить арифметическое выражение: calc "EXPRESSION"')
    calc_parser.add_argument("expression", help='выражение в кавычках, например "1 + 2 * 3"')
    calc_parser.set_defaults(func=_calculate_func)

    # python -m toolkit convert [float] [--from str] [--to str]
    conv_parser = subparsers.add_parser("convert", help="перевести из одной величины в другую: "
                                                        "convert VALUE --from UNIT --to UNIT")
    conv_parser.add_argument("value", type=float, help="значение для перевода")
    conv_parser.add_argument("--from", type=str, dest="from_unit", help='исходная единица',
                             metavar="UNIT", required=True)
    conv_parser.add_argument("--to", type=str, dest="to_unit",
                             metavar="UNIT", help="итоговая единица", required=True)
    conv_parser.set_defaults(func=_convert_func)

    args = parser.parse_args(argv)
    try:
        expression, result = args.func(args)

        if history_path is not None:
            add_entry(history_path, expression, result)
    except HistoryError as e:
        print(f"Предупреждение: {e}", file=sys.stderr)
    except ToolkitError as e:
        print(f"Ошибка: {e}", file=sys.stderr)
        return 2

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
