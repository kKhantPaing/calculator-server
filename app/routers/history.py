from collections import deque
from fastapi import APIRouter, Depends

from app.dependencies import get_history
from app.schemas import CalculatorLog

router = APIRouter()


@router.get("/history", response_model=list[CalculatorLog])
def get_history_entries(
    limit: int = 50,
    history: deque = Depends(get_history),
) -> list[CalculatorLog]:
    return list(history)[-limit:]


@router.delete("/history")
def delete_history_entries(
    history: deque = Depends(get_history),
):
    history.clear()
    return {"ok": True, "message": "History cleared"}
