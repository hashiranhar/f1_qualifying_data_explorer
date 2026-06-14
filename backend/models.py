from pydantic import BaseModel
from typing import Optional


class SessionResult(BaseModel):
    session: str
    best_lap_time: Optional[float]
    best_lap_time_fmt: Optional[str]
    participated: bool


class DriverResult(BaseModel):
    driver_code: str
    qualifying_position: Optional[int]
    sessions: list[SessionResult]


class DriversListResponse(BaseModel):
    drivers: list[str]