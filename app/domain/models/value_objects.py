from dataclasses import dataclass
from datetime import date, datetime
from typing import NewType
import uuid
from enum import Enum


EmployeeId = NewType("EmployeeId", str)
TimesheetId = NewType("TimesheetId", str)
RequestId = NewType("RequestId", str)


@dataclass(frozen=True)
class YearMonth:
    year: int
    month: int

    def __post_init__(self):
        if not (1 <= self.month <= 12):
            raise ValueError(f"Invalid month: {self.month}")
        if self.year < 1900 or self.year > 9999:
            raise ValueError(f"Invalid year: {self.year}")

    def __str__(self) -> str:
        return f"{self.year:04d}-{self.month:02d}"

    @classmethod
    def from_string(cls, value: str) -> "YearMonth":
        parts = value.split("-")
        if len(parts) != 2:
            raise ValueError(f"Invalid YearMonth format: {value}")
        return cls(year=int(parts[0]), month=int(parts[1]))


@dataclass(frozen=True)
class Date:
    value: date

    def __post_init__(self):
        if not isinstance(self.value, date):
            raise TypeError("Date value must be a datetime.date instance")

    def __str__(self) -> str:
        return self.value.isoformat()


@dataclass(frozen=True)
class DateTime:
    value: datetime

    def __post_init__(self):
        if not isinstance(self.value, datetime):
            raise TypeError("DateTime value must be a datetime.datetime instance")

    def __str__(self) -> str:
        return self.value.isoformat()

    def __lt__(self, other: "DateTime") -> bool:
        return self.value < other.value

    def __le__(self, other: "DateTime") -> bool:
        return self.value <= other.value


@dataclass(frozen=True)
class Minutes:
    value: int

    def __post_init__(self):
        if self.value < 0:
            raise ValueError(f"Minutes must be non-negative: {self.value}")


@dataclass(frozen=True)
class DateRange:
    start_date: Date
    end_date: Date

    def __post_init__(self):
        if self.start_date.value > self.end_date.value:
            raise ValueError(
                f"Start date {self.start_date} must be before or equal to end date {self.end_date}"
            )


@dataclass(frozen=True)
class TimeRange:
    start_at: DateTime
    end_at: DateTime

    def __post_init__(self):
        if self.start_at.value >= self.end_at.value:
            raise ValueError(
                f"Start time {self.start_at} must be before end time {self.end_at}"
            )

    def duration_minutes(self) -> Minutes:
        delta = self.end_at.value - self.start_at.value
        return Minutes(int(delta.total_seconds() // 60))


class EmploymentType(Enum):
    FULL_TIME = "full_time"
    CONTRACT = "contract"
    PART_TIME = "part_time"


class AttendanceState(Enum):
    CLOCKED_OUT = "clocked_out"
    CLOCKED_IN = "clocked_in"
    ON_BREAK = "on_break"


class TimesheetStatus(Enum):
    DRAFT = "draft"
    SUBMITTED = "submitted"
    APPROVED = "approved"
    REJECTED = "rejected"


class RequestStatus(Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"


class LeaveType(Enum):
    PAID = "paid"
    UNPAID = "unpaid"
    SICK = "sick"