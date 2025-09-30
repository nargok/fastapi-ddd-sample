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
from ..dtos.attendance_dtos import ClockOutRequest, ClockOutResponse
from ...domain.exceptions import InvalidStateTransitionError


class ClockOutUseCase:
    def __init__(self, timesheet_repository: TimesheetRepository):
        self.timesheet_repository = timesheet_repository

    def execute(self, request: ClockOutRequest) -> ClockOutResponse:
        try:
            employee_id = EmployeeId(request.employee_id)
            clock_out_datetime = DateTime(request.clock_out_time)
            date = Date(request.clock_out_time.date())

            year_month = YearMonth(
                year=request.clock_out_time.year,
                month=request.clock_out_time.month
            )

            timesheet = self.timesheet_repository.find_by(employee_id, year_month)

            if not timesheet:
                return ClockOutResponse(
                    success=False,
                    message="No timesheet found for this employee and month",
                    employee_id=request.employee_id,
                    date=date.value.isoformat(),
                    clock_out_time=clock_out_datetime.value.isoformat(),
                    current_state="error"
                )

            entry = timesheet.get_entry(date)
            if not entry:
                return ClockOutResponse(
                    success=False,
                    message="No attendance entry found for this date",
                    employee_id=request.employee_id,
                    date=date.value.isoformat(),
                    clock_out_time=clock_out_datetime.value.isoformat(),
                    current_state="error"
                )

            entry.clock_out(clock_out_datetime)

            worked_minutes = entry.calculate_worked_minutes()
            worked_minutes_value = worked_minutes.value if worked_minutes else None

            self.timesheet_repository.save(timesheet)

            return ClockOutResponse(
                success=True,
                message="Successfully clocked out",
                employee_id=request.employee_id,
                date=date.value.isoformat(),
                clock_out_time=clock_out_datetime.value.isoformat(),
                current_state=entry.state.value,
                worked_minutes=worked_minutes_value
            )

        except InvalidStateTransitionError as e:
            return ClockOutResponse(
                success=False,
                message=str(e),
                employee_id=request.employee_id,
                date=request.clock_out_time.date().isoformat(),
                clock_out_time=request.clock_out_time.isoformat(),
                current_state="error"
            )
        except Exception as e:
            return ClockOutResponse(
                success=False,
                message=f"An error occurred: {str(e)}",
                employee_id=request.employee_id,
                date=request.clock_out_time.date().isoformat(),
                clock_out_time=request.clock_out_time.isoformat(),
                current_state="error"
            )