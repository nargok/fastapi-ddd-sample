from dataclasses import dataclass, field
from typing import Dict
import uuid
from datetime import date as datetime_date
from .value_objects import (
    TimesheetId,
    EmployeeId,
    YearMonth,
    Date,
    TimesheetStatus,
    Minutes
)
from .attendance_entry import AttendanceEntry
from ..exceptions import (
    TimesheetAlreadySubmittedError,
    DuplicateEntryError,
    InvalidStateTransitionError
)


@dataclass
class Timesheet:
    timesheet_id: TimesheetId
    employee_id: EmployeeId
    year_month: YearMonth
    entries: Dict[datetime_date, AttendanceEntry] = field(default_factory=dict)
    status: TimesheetStatus = TimesheetStatus.DRAFT

    def __post_init__(self):
        if not self.timesheet_id:
            self.timesheet_id = TimesheetId(str(uuid.uuid4()))

        if not self.employee_id:
            raise ValueError("Employee ID is required")

        if not self.year_month:
            raise ValueError("Year-month is required")

    def add_or_update_entry(self, entry: AttendanceEntry) -> None:
        self._ensure_editable()

        entry_month = entry.date.value.month
        entry_year = entry.date.value.year

        if entry_year != self.year_month.year or entry_month != self.year_month.month:
            raise ValueError(
                f"Entry date {entry.date} does not match timesheet month {self.year_month}"
            )

        self.entries[entry.date.value] = entry

    def get_entry(self, date: Date) -> AttendanceEntry | None:
        return self.entries.get(date.value)

    def get_or_create_entry(self, date: Date) -> AttendanceEntry:
        entry = self.get_entry(date)
        if not entry:
            entry = AttendanceEntry(date=date)
            self.add_or_update_entry(entry)
        return entry

    def submit(self) -> None:
        if self.status != TimesheetStatus.DRAFT:
            raise InvalidStateTransitionError(
                f"Cannot submit timesheet with status {self.status.value}"
            )
        self.status = TimesheetStatus.SUBMITTED

    def approve(self) -> None:
        if self.status != TimesheetStatus.SUBMITTED:
            raise InvalidStateTransitionError(
                f"Cannot approve timesheet with status {self.status.value}"
            )
        self.status = TimesheetStatus.APPROVED

    def reject(self) -> None:
        if self.status != TimesheetStatus.SUBMITTED:
            raise InvalidStateTransitionError(
                f"Cannot reject timesheet with status {self.status.value}"
            )
        self.status = TimesheetStatus.REJECTED

    def reopen(self) -> None:
        if self.status != TimesheetStatus.REJECTED:
            raise InvalidStateTransitionError(
                f"Cannot reopen timesheet with status {self.status.value}"
            )
        self.status = TimesheetStatus.DRAFT

    def calculate_total_worked_minutes(self) -> Minutes:
        total = 0
        for entry in self.entries.values():
            worked = entry.calculate_worked_minutes()
            if worked:
                total += worked.value
        return Minutes(total)

    def calculate_overtime_minutes(self, standard_hours_per_day: int = 8) -> Minutes:
        total_overtime = 0
        standard_minutes = standard_hours_per_day * 60

        for entry in self.entries.values():
            worked = entry.calculate_worked_minutes()
            if worked and worked.value > standard_minutes:
                total_overtime += worked.value - standard_minutes

        return Minutes(total_overtime)

    def _ensure_editable(self) -> None:
        if self.status in [TimesheetStatus.SUBMITTED, TimesheetStatus.APPROVED]:
            raise TimesheetAlreadySubmittedError(
                f"Cannot modify timesheet with status {self.status.value}"
            )

    def is_editable(self) -> bool:
        return self.status in [TimesheetStatus.DRAFT, TimesheetStatus.REJECTED]