from datetime import datetime
from fastapi import APIRouter

try:
    from app.dependencies import aeval, history, expand_percent
    from app.schemas import Expression, CalculatorLog
except ImportError:
    from ..dependencies import aeval, history, expand_percent
    from ..schemas import Expression, CalculatorLog

router = APIRouter(tags=["calculator"])


@router.post("/calculate")
def calculate(expression: Expression):
    try:
        code = expression.expand_percent()
        result = aeval(code)
        if aeval.error:
            msg = "; ".join(str(e.get_error()) for e in aeval.error)
            aeval.error.clear()
            return {"ok": False, "expr": expression.expr, "result": "", "error": msg}
        # Add calculation to history
        record = CalculatorLog(
            timestamp=datetime.now().isoformat(),
            expr=expression.expr,
            result=result,
        )
        history.append(record)
        return {"ok": True, "expr": expression.expr, "result": result, "error": ""}
    except Exception as e:
        return {"ok": False, "expr": expression.expr, "error": str(e)}
