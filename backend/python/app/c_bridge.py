from __future__ import annotations

import ctypes
from pathlib import Path

from app.config import RISK_LIBRARY_PATH


def compute_risk_from_c(volatility: float, exposure: float, liquidity: float, default_probability: float, concentration: float) -> float | None:
    library = RISK_LIBRARY_PATH
    if not library.exists():
        return None

    try:
        lib = ctypes.CDLL(str(library))
        lib.compute_risk_score.argtypes = [ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_double]
        lib.compute_risk_score.restype = ctypes.c_double
        return float(lib.compute_risk_score(ctypes.c_double(volatility), ctypes.c_double(exposure), ctypes.c_double(liquidity), ctypes.c_double(default_probability), ctypes.c_double(concentration)))
    except (OSError, AttributeError):
        return None
