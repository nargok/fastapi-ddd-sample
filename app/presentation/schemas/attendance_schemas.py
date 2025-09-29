from pydantic import BaseModel
from datetime import datetime


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