"""Calculator server application package."""
import sys
import types
from .dependencies import expand_percent

# Alias for backwards compatibility if any legacy code imports `calculator`
if "calculator" not in sys.modules:
    _calc_mod = types.ModuleType("calculator")
    _calc_mod.expand_percent = expand_percent
    sys.modules["calculator"] = _calc_mod
