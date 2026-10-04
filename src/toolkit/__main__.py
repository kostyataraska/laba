import argparse
import sys

from toolkit.calculator import calculator
from toolkit.convertor import converting
from toolkit.errors import ToolkitError


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog='python -m toolkit',
        description='Калькулятор и конвертер величин',
    )
    commands = parser.add_subparsers(dest='command', required=True)

    calc = commands.add_parser('calc', help='Вычислить выражение')
    calc.add_argument('expression', help='Выражение, например "2 + 3 * 4"')

    conv = commands.add_parser('convert', help='Конвертировать величину')
    conv.add_argument('value', help='Число')
    conv.add_argument('--from', dest='from_unit', required=True, help='Исходная единица')
    conv.add_argument('--to', dest='to_unit', required=True, help='Целевая единица')
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        if args.command == 'calc':
            result = calculator(args.expression)
        else:
            result = converting(args.value, args.from_unit, args.to_unit)
    except ToolkitError as error:
        print(f'Ошибка: {error}', file=sys.stderr)
        return 2
    print(result)
    return 0


if __name__ == '__main__':
    sys.exit(main())
