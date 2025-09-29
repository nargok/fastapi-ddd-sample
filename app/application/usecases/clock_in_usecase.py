from datetime import datetime
from ...domain.repositories.timesheet_repository import TimesheetRepository
from ...domain.models import (
    Timesheet,
    TimesheetId,
    EmployeeId,
    YearMonth,
    Date,
    DateTime
)
from ..dtos.attendance_dtos import ClockInRequest, ClockInResponse
from ...domain.exceptions import InvalidStateTransitionError


class ClockInUseCase:
    def __init__(self, timesheet_repository: TimesheetRepository):
        self.timesheet_repository = timesheet_repository

    def execute(self, request: ClockInRequest) -> ClockInResponse:
        try:
            employee_id = EmployeeId(request.employee_id)
            clock_in_datetime = DateTime(request.clock_in_time)
            date = Date(request.clock_in_time.date())

            year_month = YearMonth(
                year=request.clock_in_time.year,
                month=request.clock_in_time.month
            )

            timesheet = self.timesheet_repository.find_by(employee_id, year_month)

            if not timesheet:
                timesheet = Timesheet(
                    timesheet_id=TimesheetId(""),
                    employee_id=employee_id,
                    year_month=year_month
                )

            entry = timesheet.get_or_create_entry(date)
            entry.clock_in(clock_in_datetime)

            self.timesheet_repository.save(timesheet)

            return ClockInResponse(
                success=True,
                message="Successfully clocked in",
                employee_id=request.employee_id,
                date=date.value.isoformat(),
                clock_in_time=clock_in_datetime.value.isoformat(),
                current_state=entry.state.value
            )

        except InvalidStateTransitionError as e:
            return ClockInResponse(
                success=False,
                message=str(e),
                employee_id=request.employee_id,
                date=request.clock_in_time.date().isoformat(),
                clock_in_time=request.clock_in_time.isoformat(),
                current_state="error"
            )
        except Exception as e:
            return ClockInResponse(
                success=False,
                message=f"An error occurred: {str(e)}",
                employee_id=request.employee_id,
                date=request.clock_in_time.date().isoformat(),
                clock_in_time=request.clock_in_time.isoformat(),
                current_state="error"
            )