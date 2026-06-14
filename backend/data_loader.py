import json
import logging
from pathlib import Path
from typing import Optional

logger = logging.getLogger(__name__)


def load_json(path: str) -> dict:
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"Data file not found: {path}")
    with open(p, "r", encoding="utf-8") as f:
        return json.load(f)


def _to_float(value) -> Optional[float]:
    try:
        f = float(value)
        return f if f > 0 else None
    except (TypeError, ValueError):
        return None


def _is_present(value) -> bool:
    return value is not None and str(value) != "None"


def _format_laptime(seconds: float) -> str:
    minutes = int(seconds // 60)
    remaining = seconds - (minutes * 60)
    return f"{minutes}:{remaining:06.3f}"


def _is_valid_lap(index: int, data: dict) -> bool:
    if _to_float(data["time"][index]) is None:
        return False
    if not data["iacc"][index]:
        return False
    if _is_present(data["pout"][index]):
        return False
    if _is_present(data["pin"][index]):
        return False
    return True


def get_all_drivers(data: dict) -> list[str]:
    return sorted(set(data["drv"]))


def get_driver_result(data: dict, driver_code: str) -> Optional[dict]:
    code = driver_code.strip().upper()
    total = len(data["drv"])

    if code not in data["drv"]:
        return None

    best: dict[str, Optional[float]] = {"Q1": None, "Q2": None, "Q3": None}
    participated: dict[str, bool] = {"Q1": False, "Q2": False, "Q3": False}

    for i in range(total):
        if data["drv"][i] != code:
            continue
        session = data["qs"][i]
        if session not in best:
            continue
        participated[session] = True
        if not _is_valid_lap(i, data):
            continue
        t = _to_float(data["time"][i])
        if best[session] is None or t < best[session]:
            best[session] = t

    sessions = [
        {
            "session": s,
            "best_lap_time": best[s],
            "best_lap_time_fmt": _format_laptime(best[s]) if best[s] else None,
            "participated": participated[s],
        }
        for s in ["Q1", "Q2", "Q3"]
    ]

    return {
        "driver_code": code,
        "qualifying_position": _derive_position(data, code),
        "sessions": sessions,
    }


def _derive_position(data: dict, target_code: str) -> Optional[int]:
    total = len(data["drv"])
    best: dict[str, dict[str, Optional[float]]] = {}

    for i in range(total):
        d, s = data["drv"][i], data["qs"][i]
        if d not in best:
            best[d] = {"Q1": None, "Q2": None, "Q3": None}
        if s not in best[d] or not _is_valid_lap(i, data):
            continue
        t = _to_float(data["time"][i])
        if t and (best[d][s] is None or t < best[d][s]):
            best[d][s] = t

    q3 = {d: best[d]["Q3"] for d in best if best[d]["Q3"] is not None}
    q2 = {d: best[d]["Q2"] for d in best if d not in q3 and best[d]["Q2"] is not None}
    q1 = {d: best[d]["Q1"] for d in best if d not in q3 and d not in q2 and best[d]["Q1"] is not None}

    ranked = (
        sorted(q3, key=lambda d: q3[d]) +
        sorted(q2, key=lambda d: q2[d]) +
        sorted(q1, key=lambda d: q1[d])
    )

    return ranked.index(target_code) + 1 if target_code in ranked else None