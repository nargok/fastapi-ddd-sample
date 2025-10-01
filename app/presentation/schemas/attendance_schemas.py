from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class ClockInRequest(BaseModel):
    clock_in_time: datetime

    class Config:
        json_schema_extra = {
            "example": {
                "clock_in_time": "2024-01-15T09:00:00"
            }
        }


class ClockInResponse(BaseModel):
    success: bool
    message: str
    employee_id: str
    date: str
    clock_in_time: str
    current_state: str

    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "message": "Successfully clocked in",
                "employee_id": "EMP001",
                "date": "2024-01-15",
                "clock_in_time": "2024-01-15T09:00:00",
                "current_state": "clocked_in"
            }
        }


class ClockOutRequest(BaseModel):
    clock_out_time: datetime

    class Config:
        json_schema_extra = {
            "example": {
                "clock_out_time": "2024-01-15T18:00:00"
            }
        }


class ClockOutResponse(BaseModel):
    success: bool
    message: str
    employee_id: str
    date: str
    clock_out_time: str
    current_state: str
    worked_minutes: Optional[int] = None

    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "message": "Successfully clocked out",
                "employee_id": "EMP001",
                "date": "2024-01-15",
                "clock_out_time": "2024-01-15T18:00:00",
                "current_state": "clocked_out",
                "worked_minutes": 480
            }
        }


class StartBreakRequest(BaseModel):
    break_start_time: datetime

    class Config:
        json_schema_extra = {
            "example": {
                "break_start_time": "2024-01-15T12:00:00"
            }
        }


class StartBreakResponse(BaseModel):
    success: bool
    message: str
    employee_id: str
    date: str
    break_start_time: str
    current_state: str

    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "message": "Successfully started break",
                "employee_id": "EMP001",
                "date": "2024-01-15",
                "break_start_time": "2024-01-15T12:00:00",
                "current_state": "on_break"
            }
        }


class EndBreakRequest(BaseModel):
    break_end_time: datetime

    class Config:
        json_schema_extra = {
            "example": {
                "break_end_time": "2024-01-15T13:00:00"
            }
        }


class EndBreakResponse(BaseModel):
    success: bool
    message: str
    employee_id: str
    date: str
    break_end_time: str
    current_state: str
    break_duration_minutes: Optional[int] = None

    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "message": "Successfully ended break",
                "employee_id": "EMP001",
                "date": "2024-01-15",
                "break_end_time": "2024-01-15T13:00:00",
                "current_state": "clocked_in",
                "break_duration_minutes": 60
            }
        }