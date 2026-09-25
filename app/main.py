import math
from collections import deque
from datetime import datetime
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from asteval import Interpreter

from calculator import expand_percent

from models import Expression, CalculatorLog

HISTORY_MAX = 1000
# HISTORY (in-memory for now)
history = deque(maxlen=HISTORY_MAX)

app = FastAPI(title="Mini Calculator API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------- Safe evaluator ----------
aeval = Interpreter(minimal=True, usersyms={"pi": math.pi, "e": math.e})

@app.post("/calculate")
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

# GET /history
@app.get("/history", response_model=list[CalculatorLog])
def get_history(limit: int = 50) -> list[CalculatorLog]:
    return list(history)[-limit:]

# DELETE /history
@app.delete("/history")
def delete_history():
    history.clear()
    return {"ok": True, "message": "History cleared"}
