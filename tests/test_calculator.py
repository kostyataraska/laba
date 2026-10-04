import pytest

from toolkit.calculator import calculator
from toolkit.errors import (
    DivisionByZeroError,
    EmptyExpressionError,
    InvalidCharacterAfterDotError,
    InvalidCharacterError,
    MissingOperandError,
    MissingOperatorError,
    TwoOperatorsError,
)


@pytest.mark.parametrize(
    'expr, expected',
    [
        ('100', 100.0),
        ('2 + 3', 5.0),
        ('  2   *  3 ', 6.0),
        ('1.5 + 2.25', 3.75),
        ('3 + 4 * 2', 11.0),
        ('10 / 4 + 2', 4.5),
        ('7 + 8 / 4 - 1', 8.0),
        ('8 - 3 - 2', 3.0),
    ],
)
def test_basic_calculations(expr, expected):
    assert calculator(expr) == pytest.approx(expected)


@pytest.mark.parametrize(
    'expr, expected',
    [
        ('-5', -5.0),
        ('+5', 5.0),
        ('5 -3', 2.0),
        ('2 * -3', -6.0),
        ('2*-55', -110.0),
        ('1 - -2', 3.0),
        ('-5 + 2 * -3', -11.0),
    ],
)
def test_negative_operands(expr, expected):
    assert calculator(expr) == pytest.approx(expected)


@pytest.mark.parametrize(
    'expr, expected',
    [
        ('7 // 2', 3.0),
        ('-7 // 3', -3.0),
        ('7 // -2', -4.0),
        ('-7 % 3', 2.0),
        ('1 + 7 // 2', 4.0),
    ],
)
def test_floor_division_and_modulo(expr, expected):
    assert calculator(expr) == pytest.approx(expected)


def test_result_is_float():
    assert isinstance(calculator('2 + 3'), float)


@pytest.mark.parametrize(
    'expr, error',
    [
        ('', EmptyExpressionError),
        ('   ', EmptyExpressionError),
        ('abc', InvalidCharacterError),
        ('2 ^ 3', InvalidCharacterError),
        ('2 +', MissingOperandError),
        ('* 3', MissingOperandError),
        ('2 * / 3', TwoOperatorsError),
        ('1 2', MissingOperatorError),
        ('1.', InvalidCharacterAfterDotError),
    ],
)
def test_invalid_expressions(expr, error):
    with pytest.raises(error):
        calculator(expr)


@pytest.mark.parametrize('expr', ['1 / 0', '1 // 0', '5 % 0'])
def test_division_by_zero(expr):
    with pytest.raises(DivisionByZeroError):
        calculator(expr)