from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from ..schemas.attendance_schemas import (
    ClockInRequest, ClockInResponse,
    ClockOutRequest, ClockOutResponse
)
from ..dependencies import get_timesheet_repository, get_current_employee_id
from ...domain.repositories.timesheet_repository import TimesheetRepository
from ...application.usecases import ClockInUseCase
from ...application.usecases.clock_out_usecase import ClockOutUseCase
from ...application.dtos import attendance_dtos

router = APIRouter(
    prefix="/v1/attendance",
    tags=["attendance"]
)


@router.post("/clock-in", response_model=ClockInResponse)
def clock_in(
    request: ClockInRequest,
    employee_id: Annotated[str, Depends(get_current_employee_id)],
    repository: Annotated[TimesheetRepository, Depends(get_timesheet_repository)]
) -> ClockInResponse:
    use_case = ClockInUseCase(repository)

    dto_request = attendance_dtos.ClockInRequest(
        employee_id=employee_id,
        clock_in_time=request.clock_in_time
    )

    dto_response = use_case.execute(dto_request)

    if not dto_response.success:
        raise HTTPException(status_code=400, detail=dto_response.message)

    return ClockInResponse(
        success=dto_response.success,
        message=dto_response.message,
        employee_id=dto_response.employee_id,
        date=dto_response.date,
        clock_in_time=dto_response.clock_in_time,
        current_state=dto_response.current_state
    )


@router.post("/clock-out", response_model=ClockOutResponse)
def clock_out(
    request: ClockOutRequest,
    employee_id: Annotated[str, Depends(get_current_employee_id)],
    repository: Annotated[TimesheetRepository, Depends(get_timesheet_repository)]
) -> ClockOutResponse:
    use_case = ClockOutUseCase(repository)

    dto_request = attendance_dtos.ClockOutRequest(
        employee_id=employee_id,
        clock_out_time=request.clock_out_time
    )

    dto_response = use_case.execute(dto_request)

    if not dto_response.success:
        raise HTTPException(status_code=400, detail=dto_response.message)

    return ClockOutResponse(
        success=dto_response.success,
        message=dto_response.message,
        employee_id=dto_response.employee_id,
        date=dto_response.date,
        clock_out_time=dto_response.clock_out_time,
        current_state=dto_response.current_state,
        worked_minutes=dto_response.worked_minutes
    )