from collections import deque
from datetime import datetime
from fastapi import APIRouter, Depends

from app.dependencies import aeval, expand_percent, get_history
from app.schemas import Expression, CalculatorLog

router = APIRouter()


@router.post("/calculate")
def calculate(
    expression: Expression,
    history: deque = Depends(get_history),
):
    try:
        code = expand_percent(expression.expr)
        result = aeval(code)
        if aeval.error:
            msg = "; ".join(str(e.get_error()) for e in aeval.error)
            aeval.error.clear()
            return {"ok": False, "expr": expression.expr, "result": "", "error": msg}

        record = CalculatorLog(
            timestamp=datetime.now().isoformat(),
            expr=expression.expr,
            result=result,
        )
        history.append(record)
        return {"ok": True, "expr": expression.expr, "result": result, "error": ""}
    except Exception as e:
        return {"ok": False, "expr": expression.expr, "error": str(e)}
