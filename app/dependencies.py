import math
import re
from collections import deque
from asteval import Interpreter

# Safe evaluator
aeval = Interpreter(minimal=True, usersyms={"pi": math.pi, "e": math.e})

# In-memory history
HISTORY_MAX = 1000
history = deque(maxlen=HISTORY_MAX)


def get_history() -> deque:
    return history


# Percent expansion
_percent_pair = re.compile(
    r"(?P<a>\d+(?:\.\d+)?)\s*(?P<op>[+\-*/])\s*(?P<b>\d+(?:\.\d+)?)%"
)
_number_percent = re.compile(r"(?P<n>\d+(?:\.\d+)?)%")


def expand_percent(expr: str) -> str:
    s = expr
    while True:
        m = _percent_pair.search(s)
        if not m:
            break
        a, op, b = m.group("a", "op", "b")
        if op in "+-":
            repl = f"{a} {op} (({b}/100)*{a})"
        elif op == "*":
            repl = f"{a} * ({b}/100)"
        else:
            repl = f"{a} / ({b}/100)"
        s = s[: m.start()] + repl + s[m.end() :]

    return _number_percent.sub(lambda m: f"({m.group('n')}/100)", s)
