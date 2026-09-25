from pydantic import BaseModel


class BaseExpression(BaseModel):
    expr: str


class ExpressionIn(BaseExpression):
    pass


# Expression is ExpressionIn
Expression = ExpressionIn


class ExpressionOut(Expression):
    result: float | int
    timestamp: str | None = None


# CalculatorLog is ExpressionOut, which is a subclass of Expression
CalculatorLog = ExpressionOut
