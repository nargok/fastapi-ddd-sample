from datetime import datetime
from ...domain.repositories.timesheet_repository import TimesheetRepository
from ...domain.models import (
    EmployeeId,
    YearMonth,
    Date,
    DateTime
)
from ..dtos.attendance_dtos import EndBreakRequest, EndBreakResponse
from ...domain.exceptions import InvalidStateTransitionError, InvalidTimeRangeError


class EndBreakUseCase:
    def __init__(self, timesheet_repository: TimesheetRepository):
        self.timesheet_repository = timesheet_repository

    def execute(self, request: EndBreakRequest) -> EndBreakResponse:
        try:
            employee_id = EmployeeId(request.employee_id)
            break_end_datetime = DateTime(request.break_end_time)
            date = Date(request.break_end_time.date())

            year_month = YearMonth(
                year=request.break_end_time.year,
                month=request.break_end_time.month
            )

            timesheet = self.timesheet_repository.find_by(employee_id, year_month)

            if not timesheet:
                return EndBreakResponse(
                    success=False,
                    message="No timesheet found for this employee and month",
                    employee_id=request.employee_id,
                    date=date.value.isoformat(),
                    break_end_time=break_end_datetime.value.isoformat(),
                    current_state="error"
                )

            entry = timesheet.get_entry(date)
            if not entry:
                return EndBreakResponse(
                    success=False,
                    message="No attendance entry found for this date",
                    employee_id=request.employee_id,
                    date=date.value.isoformat(),
                    break_end_time=break_end_datetime.value.isoformat(),
                    current_state="error"
                )

            # Get the ongoing break to calculate duration
            ongoing_break = None
            for break_interval in entry.breaks:
                if break_interval.is_ongoing():
                    ongoing_break = break_interval
                    break

            entry.end_break(break_end_datetime)
            self.timesheet_repository.save(timesheet)

            # Calculate the break duration if we found the ongoing break
            break_duration_minutes = None
            if ongoing_break:
                # The break has now been ended, so we can get its duration
                for break_interval in entry.breaks:
                    if break_interval.start_at == ongoing_break.start_at:
                        duration = break_interval.duration_minutes()
                        if duration:
                            break_duration_minutes = duration.value
                        break

            return EndBreakResponse(
                success=True,
                message="Successfully ended break",
                employee_id=request.employee_id,
                date=date.value.isoformat(),
                break_end_time=break_end_datetime.value.isoformat(),
                current_state=entry.state.value,
                break_duration_minutes=break_duration_minutes
            )

        except InvalidStateTransitionError as e:
            return EndBreakResponse(
                success=False,
                message=str(e),
                employee_id=request.employee_id,
                date=request.break_end_time.date().isoformat(),
                break_end_time=request.break_end_time.isoformat(),
                current_state="error"
            )
        except InvalidTimeRangeError as e:
            return EndBreakResponse(
                success=False,
                message=str(e),
                employee_id=request.employee_id,
                date=request.break_end_time.date().isoformat(),
                break_end_time=request.break_end_time.isoformat(),
                current_state="error"
            )
        except Exception as e:
            return EndBreakResponse(
                success=False,
                message=f"An error occurred: {str(e)}",
                employee_id=request.employee_id,
                date=request.break_end_time.date().isoformat(),
                break_end_time=request.break_end_time.isoformat(),
                current_state="error"
            )