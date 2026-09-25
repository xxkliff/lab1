
import argparse
import sys

from toolkit.converter import convert
from toolkit.calculator import evaluate
from toolkit.errors import ToolkitError

def _convert_func(args) -> None:
    result = convert(args.value, args.from_unit, args.to_unit)
    print(f"{args.value:.10g} {args.from_unit} -> {result:.10g} {args.to_unit}")

def _calculate_func(args) -> None:
    result = evaluate(args.expression)
    print(f"{result:.10g}")

def main() -> int:
    """
    Обязательнная составляющая программ, которые сдаются. Является точкой входа в приложение
    :return: Данная функция ничего не возвращает
    """
    parser = argparse.ArgumentParser(
        prog="toolkit",
        description="Набор утилит: калькулятор и конвертор единиц")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # python3.14 -m toolkit calc "expression"
    calc_parser = subparsers.add_parser("calc", help="вычислить арифметическое выражение")
    calc_parser.add_argument("expression", help='выражение в кавычках, например "1 + 2 * 3"')
    calc_parser.set_defaults(func=_calculate_func)

    # python3.14 -m toolkit convert [float] [--from str] [--to str]
    conv_parser = subparsers.add_parser("convert", help="перевести из одной величины в другую")
    conv_parser.add_argument('value', type=float, help='значение для перевода')
    conv_parser.add_argument('--from', type=str, dest="from_unit", help='исходная единица')
    conv_parser.add_argument('--to', type=str, dest="to_unit", help='итоговая единица')
    conv_parser.set_defaults(func=_convert_func)

    args = parser.parse_args()
    try:
        args.func(args)
    except ToolkitError as e:
        print(f"Ошибка: {e}", file=sys.stderr)
        return 2

    return 0

if __name__ == "__main__":
    main()
