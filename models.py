from datetime import datetime
from pydantic import BaseModel
from calculator import expand_percent


class Expression(BaseModel):
    expr: str

    def expand_percent(self) -> str:
        """Return the expression string after expanding % symbols."""
        return expand_percent(self.expr)


class CalculatorLog(BaseModel):
    timestamp: str | None = None
    expr: str
    result: float | int
