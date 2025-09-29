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