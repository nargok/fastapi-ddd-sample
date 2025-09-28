from abc import ABC, abstractmethod
from typing import Optional
from ..models import Timesheet, EmployeeId, YearMonth


class TimesheetRepository(ABC):

    @abstractmethod
    def find_by(self, employee_id: EmployeeId, year_month: YearMonth) -> Optional[Timesheet]:
        """Find timesheet by employee ID and year-month"""
        pass

    @abstractmethod
    def save(self, timesheet: Timesheet) -> None:
        """Save or update timesheet"""
        pass