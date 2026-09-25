from app.dependencies import expand_percent
from app.schemas import BaseExpression, ExpressionIn, ExpressionOut, Expression, CalculatorLog


def test_add_percent():
    assert expand_percent("5 + 10%") == "5 + ((10/100)*5)"


def test_subtract_percent():
    assert expand_percent("20 - 30%") == "20 - ((30/100)*20)"


def test_multiply_percent():
    assert expand_percent("15 * 25%") == "15 * (25/100)"


def test_divide_percent():
    assert expand_percent("40 / 50%") == "40 / (50/100)"


def test_multiple_operations():
    assert expand_percent("3 * 4% + 2 / 1%") == "3 * (4/100) + 2 / (1/100)"


def test_standalone_percent():
    assert expand_percent("100%") == "(100/100)"


def test_multiple_standalone_percents():
    assert expand_percent("10% + 20%") == "(10/100) + (20/100)"


def test_expression_inheritance():
    assert issubclass(ExpressionIn, BaseExpression)
    assert issubclass(ExpressionOut, BaseExpression)
    assert issubclass(ExpressionOut, ExpressionIn)
    assert issubclass(CalculatorLog, Expression)
    assert Expression is ExpressionIn
    assert CalculatorLog is ExpressionOut
