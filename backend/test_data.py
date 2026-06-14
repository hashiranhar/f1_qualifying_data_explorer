import pytest
from data_loader import (
    _to_float,
    _is_present,
    _format_laptime,
    _is_valid_lap,
    get_all_drivers,
    get_driver_result,
)

# ── Minimal fake dataset mirroring real structure ──────────────────────────────
MOCK_DATA = {
    "drv":  ["HAM", "HAM", "HAM", "VER", "VER"],
    "qs":   ["Q1",  "Q1",  "Q2",  "Q1",  "Q1"],
    "time": [80.5,  79.1,  78.3,  81.0,  "None"],
    "iacc": [True,  True,  True,  False,  True],
    "pout": ["None","None","None","None","None"],
    "pin":  ["None","None","None","None","None"],
}


def test_to_float_valid():
    assert _to_float(80.5) == 80.5

def test_to_float_string_none():
    assert _to_float("None") is None

def test_to_float_zero():
    assert _to_float(0) is None

def test_to_float_invalid():
    assert _to_float("bad") is None


def test_is_present_none():
    assert _is_present(None) is False

def test_is_present_string_none():
    assert _is_present("None") is False

def test_is_present_valid():
    assert _is_present(768.6) is True


def test_format_laptime():
    assert _format_laptime(79.453) == "1:19.453"

def test_format_laptime_sub_minute():
    assert _format_laptime(59.1) == "0:59.100"


def test_valid_lap_passes():
    assert _is_valid_lap(0, MOCK_DATA) is True

def test_invalid_lap_iacc_false():
    assert _is_valid_lap(3, MOCK_DATA) is False

def test_invalid_lap_null_time():
    assert _is_valid_lap(4, MOCK_DATA) is False

def test_invalid_lap_pit_out():
    data = {**MOCK_DATA, "pout": ["768.6", "None", "None", "None", "None"]}
    assert _is_valid_lap(0, data) is False

def test_invalid_lap_pit_in():
    data = {**MOCK_DATA, "pin": ["None", "900.1", "None", "None", "None"]}
    assert _is_valid_lap(1, data) is False


def test_get_all_drivers():
    assert get_all_drivers(MOCK_DATA) == ["HAM", "VER"]


def test_unknown_driver_returns_none():
    assert get_driver_result(MOCK_DATA, "ZZZ") is None

def test_driver_code_normalised():
    assert get_driver_result(MOCK_DATA, " ham ") is not None

def test_best_lap_selected():
    result = get_driver_result(MOCK_DATA, "HAM")
    q1 = next(s for s in result["sessions"] if s["session"] == "Q1")
    assert q1["best_lap_time"] == 79.1

def test_no_valid_laps_returns_none_time():
    result = get_driver_result(MOCK_DATA, "VER")
    q1 = next(s for s in result["sessions"] if s["session"] == "Q1")
    assert q1["best_lap_time"] is None

def test_session_not_participated():
    result = get_driver_result(MOCK_DATA, "VER")
    q2 = next(s for s in result["sessions"] if s["session"] == "Q2")
    assert q2["participated"] is False

def test_laptime_fmt_present_when_valid():
    result = get_driver_result(MOCK_DATA, "HAM")
    q1 = next(s for s in result["sessions"] if s["session"] == "Q1")
    assert q1["best_lap_time_fmt"] == "1:19.100"