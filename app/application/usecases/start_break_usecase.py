from datetime import datetime
from ...domain.repositories.timesheet_repository import TimesheetRepository
from ...domain.models import (
    EmployeeId,
    YearMonth,
    Date,
    DateTime
)
from ..dtos.attendance_dtos import StartBreakRequest, StartBreakResponse
from ...domain.exceptions import InvalidStateTransitionError, InvalidTimeRangeError


class StartBreakUseCase:
    def __init__(self, timesheet_repository: TimesheetRepository):
        self.timesheet_repository = timesheet_repository

    def execute(self, request: StartBreakRequest) -> StartBreakResponse:
        try:
            employee_id = EmployeeId(request.employee_id)
            break_start_datetime = DateTime(request.break_start_time)
            date = Date(request.break_start_time.date())

            year_month = YearMonth(
                year=request.break_start_time.year,
                month=request.break_start_time.month
            )

            timesheet = self.timesheet_repository.find_by(employee_id, year_month)

            if not timesheet:
                return StartBreakResponse(
                    success=False,
                    message="No timesheet found for this employee and month",
                    employee_id=request.employee_id,
                    date=date.value.isoformat(),
                    break_start_time=break_start_datetime.value.isoformat(),
                    current_state="error"
                )

            entry = timesheet.get_entry(date)
            if not entry:
                return StartBreakResponse(
                    success=False,
                    message="No attendance entry found for this date. Please clock in first.",
                    employee_id=request.employee_id,
                    date=date.value.isoformat(),
                    break_start_time=break_start_datetime.value.isoformat(),
                    current_state="error"
                )

            entry.start_break(break_start_datetime)
            self.timesheet_repository.save(timesheet)

            return StartBreakResponse(
                success=True,
                message="Successfully started break",
                employee_id=request.employee_id,
                date=date.value.isoformat(),
                break_start_time=break_start_datetime.value.isoformat(),
                current_state=entry.state.value
            )

        except InvalidStateTransitionError as e:
            return StartBreakResponse(
                success=False,
                message=str(e),
                employee_id=request.employee_id,
                date=request.break_start_time.date().isoformat(),
                break_start_time=request.break_start_time.isoformat(),
                current_state="error"
            )
        except InvalidTimeRangeError as e:
            return StartBreakResponse(
                success=False,
                message=str(e),
                employee_id=request.employee_id,
                date=request.break_start_time.date().isoformat(),
                break_start_time=request.break_start_time.isoformat(),
                current_state="error"
            )
        except Exception as e:
            return StartBreakResponse(
                success=False,
                message=f"An error occurred: {str(e)}",
                employee_id=request.employee_id,
                date=request.break_start_time.date().isoformat(),
                break_start_time=request.break_start_time.isoformat(),
                current_state="error"
            )