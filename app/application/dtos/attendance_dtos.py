from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class ClockInRequest:
    employee_id: str
    clock_in_time: datetime


@dataclass
class ClockInResponse:
    success: bool
    message: str
    employee_id: str
    date: str
    clock_in_time: str
    current_state: str


@dataclass
class ClockOutRequest:
    employee_id: str
    clock_out_time: datetime


@dataclass
class ClockOutResponse:
    success: bool
    message: str
    employee_id: str
    date: str
    clock_out_time: str
    current_state: str
    worked_minutes: Optional[int] = None