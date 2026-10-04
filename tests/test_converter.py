import pytest

from toolkit.convertor import converting
from toolkit.errors import (
    BelowAbsoluteZeroError,
    IncompatibleUnitsError,
    InvalidValueError,
    UnknownUnitError,
)


@pytest.mark.parametrize(
    'value, from_unit, to_unit, expected',
    [
        (1, 'km', 'm', 1000.0),
        (1000, 'm', 'km', 1.0),
        (250, 'cm', 'm', 2.5),
        (5, 'mm', 'cm', 0.5),
        (1500, 'g', 'kg', 1.5),
        (2, 'kg', 'g', 2000.0),
        (5, 'm', 'm', 5.0),
    ],
)
def test_convert_length_and_mass(value, from_unit, to_unit, expected):
    assert converting(value, from_unit, to_unit) == pytest.approx(expected)


@pytest.mark.parametrize(
    'value, from_unit, to_unit, expected',
    [
        (0, 'c', 'f', 32.0),
        (100, 'c', 'f', 212.0),
        (32, 'f', 'c', 0.0),
        (-40, 'c', 'f', -40.0),
        (0, 'c', 'k', 273.15),
        (273.15, 'k', 'c', 0.0),
        (0, 'k', 'c', -273.15),
        (-273.15, 'c', 'k', 0.0),   # ровно абсолютный ноль допустим
    ],
)
def test_convert_temperature(value, from_unit, to_unit, expected):
    assert converting(value, from_unit, to_unit) == pytest.approx(expected)


def test_units_are_case_insensitive():
    assert converting(1, 'KM', 'M') == pytest.approx(1000.0)


def test_value_can_be_a_string():
    assert converting('2.5', 'm', 'cm') == pytest.approx(250.0)


def test_convert_returns_float():
    assert isinstance(converting(1, 'm', 'm'), float)


@pytest.mark.parametrize(
    'value, from_unit, to_unit, error',
    [
        (1, 'm', 'kg', IncompatibleUnitsError),
        (1, 'c', 'm', IncompatibleUnitsError),
        (1, 'foo', 'm', UnknownUnitError),
        (1, 'm', 'bar', UnknownUnitError),
        ('abc', 'm', 'km', InvalidValueError),
        ('', 'm', 'km', InvalidValueError),
        ('nan', 'm', 'km', InvalidValueError),
        ('inf', 'm', 'km', InvalidValueError),
        (-273.16, 'c', 'k', BelowAbsoluteZeroError),
        (-1, 'k', 'c', BelowAbsoluteZeroError),
        (-460, 'f', 'c', BelowAbsoluteZeroError),
    ],
)
def test_convert_errors(value, from_unit, to_unit, error):
    with pytest.raises(error):
        converting(value, from_unit, to_unit)