import math

from toolkit.errors import (
    BelowAbsoluteZeroError,
    IncompatibleUnitsError,
    InvalidValueError,
    UnknownUnitError,
)

LENGTH_IN_METERS = {'mm': 0.001, 'cm': 0.01, 'm': 1.0, 'km': 1000.0}
MASS_IN_KILOGRAMS = {'g': 0.001, 'kg': 1.0}
TEMPERATURE_UNITS = ('c', 'f', 'k')

EPSILON = 1e-9  # ошибка округления при проверке абсолютного нуля


def parse_value(value: str | float) -> float:
    try:
        number = float(value)
    except (TypeError, ValueError):
        raise InvalidValueError(f'Неверное числовое значение: {value!r}') from None
    if not math.isfinite(number):
        raise InvalidValueError(f'Неверное числовое значение: {value!r}')
    return number


def find_group(unit: str) -> str:
    if unit in LENGTH_IN_METERS:
        return 'length'
    if unit in MASS_IN_KILOGRAMS:
        return 'mass'
    if unit in TEMPERATURE_UNITS:
        return 'temperature'
    raise UnknownUnitError(f'Неизвестная единица: {unit!r}')


def to_kelvin(value: float, unit: str) -> float:
    if unit == 'c':
        return value + 273.15
    if unit == 'f':
        return (value - 32) * 5 / 9 + 273.15
    return value


def from_kelvin(kelvin: float, unit: str) -> float:
    if unit == 'c':
        return kelvin - 273.15
    if unit == 'f':
        return (kelvin - 273.15) * 9 / 5 + 32
    return kelvin


def converting_temperature(value: float, from_unit: str, to_unit: str) -> float:
    kelvin = to_kelvin(value, from_unit)
    if kelvin < -EPSILON:
        raise BelowAbsoluteZeroError('Температура ниже абсолютного нуля')
    return from_kelvin(kelvin, to_unit)


def converting(value: str | float, from_unit: str, to_unit: str) -> float:
    from_unit = from_unit.strip().lower()
    to_unit = to_unit.strip().lower()
    number = parse_value(value)

    from_group = find_group(from_unit)
    to_group = find_group(to_unit)
    if from_group != to_group:
        raise IncompatibleUnitsError(f'Нельзя перевести {from_unit} в {to_unit}')

    if from_group == 'length':
        return number * LENGTH_IN_METERS[from_unit] / LENGTH_IN_METERS[to_unit]
    if from_group == 'mass':
        return number * MASS_IN_KILOGRAMS[from_unit] / MASS_IN_KILOGRAMS[to_unit]
    return converting_temperature(number, from_unit, to_unit)
