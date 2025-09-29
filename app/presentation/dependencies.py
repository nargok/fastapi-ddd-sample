from typing import Annotated
from fastapi import Depends, Header, HTTPException
from ..infrastructure.repositories import InMemoryTimesheetRepository
from ..domain.repositories.timesheet_repository import TimesheetRepository


_timesheet_repository = InMemoryTimesheetRepository()


def get_timesheet_repository() -> TimesheetRepository:
    return _timesheet_repository


def get_current_employee_id(
    x_employee_id: Annotated[str | None, Header()] = None
) -> str:
    if not x_employee_id:
        raise HTTPException(
            status_code=400,
            detail="X-Employee-ID header is required"
        )
    return x_employee_id