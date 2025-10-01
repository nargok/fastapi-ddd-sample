from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from ..schemas.attendance_schemas import (
    ClockInRequest, ClockInResponse,
    ClockOutRequest, ClockOutResponse,
    StartBreakRequest, StartBreakResponse,
    EndBreakRequest, EndBreakResponse
)
from ..dependencies import get_timesheet_repository, get_current_employee_id
from ...domain.repositories.timesheet_repository import TimesheetRepository
from ...application.usecases import ClockInUseCase
from ...application.usecases.clock_out_usecase import ClockOutUseCase
from ...application.usecases.start_break_usecase import StartBreakUseCase
from ...application.usecases.end_break_usecase import EndBreakUseCase
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


@router.post("/start-break", response_model=StartBreakResponse)
def start_break(
    request: StartBreakRequest,
    employee_id: Annotated[str, Depends(get_current_employee_id)],
    repository: Annotated[TimesheetRepository, Depends(get_timesheet_repository)]
) -> StartBreakResponse:
    use_case = StartBreakUseCase(repository)

    dto_request = attendance_dtos.StartBreakRequest(
        employee_id=employee_id,
        break_start_time=request.break_start_time
    )

    dto_response = use_case.execute(dto_request)

    if not dto_response.success:
        raise HTTPException(status_code=400, detail=dto_response.message)

    return StartBreakResponse(
        success=dto_response.success,
        message=dto_response.message,
        employee_id=dto_response.employee_id,
        date=dto_response.date,
        break_start_time=dto_response.break_start_time,
        current_state=dto_response.current_state
    )


@router.post("/end-break", response_model=EndBreakResponse)
def end_break(
    request: EndBreakRequest,
    employee_id: Annotated[str, Depends(get_current_employee_id)],
    repository: Annotated[TimesheetRepository, Depends(get_timesheet_repository)]
) -> EndBreakResponse:
    use_case = EndBreakUseCase(repository)

    dto_request = attendance_dtos.EndBreakRequest(
        employee_id=employee_id,
        break_end_time=request.break_end_time
    )

    dto_response = use_case.execute(dto_request)

    if not dto_response.success:
        raise HTTPException(status_code=400, detail=dto_response.message)

    return EndBreakResponse(
        success=dto_response.success,
        message=dto_response.message,
        employee_id=dto_response.employee_id,
        date=dto_response.date,
        break_end_time=dto_response.break_end_time,
        current_state=dto_response.current_state,
        break_duration_minutes=dto_response.break_duration_minutes
    )