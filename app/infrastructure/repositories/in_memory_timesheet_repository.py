from typing import Optional, Dict, Tuple
from ...domain.repositories.timesheet_repository import TimesheetRepository
from ...domain.models import Timesheet, EmployeeId, YearMonth


class InMemoryTimesheetRepository(TimesheetRepository):
    def __init__(self):
        self._storage: Dict[Tuple[str, str], Timesheet] = {}

    def find_by(self, employee_id: EmployeeId, year_month: YearMonth) -> Optional[Timesheet]:
        key = self._create_key(employee_id, year_month)
        return self._storage.get(key)

    def save(self, timesheet: Timesheet) -> None:
        key = self._create_key(timesheet.employee_id, timesheet.year_month)
        self._storage[key] = timesheet

    def _create_key(self, employee_id: EmployeeId, year_month: YearMonth) -> Tuple[str, str]:
        year_month_str = f"{year_month.year:04d}-{year_month.month:02d}"
        return (employee_id, year_month_str)