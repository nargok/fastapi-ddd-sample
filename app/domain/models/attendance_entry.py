from dataclasses import dataclass, field
from typing import List
from .value_objects import Date, DateTime, AttendanceState, Minutes
from .break_interval import BreakInterval
from ..exceptions import (
    InvalidStateTransitionError,
    InvalidTimeRangeError,
    OverlappingBreaksError
)


@dataclass
class AttendanceEntry:
    date: Date
    state: AttendanceState = AttendanceState.CLOCKED_OUT
    clock_in_at: DateTime | None = None
    clock_out_at: DateTime | None = None
    breaks: List[BreakInterval] = field(default_factory=list)
    notes: str = ""

    def __post_init__(self):
        if self.clock_in_at and self.clock_out_at:
            if self.clock_in_at >= self.clock_out_at:
                raise InvalidTimeRangeError(
                    f"Clock in time {self.clock_in_at} must be before clock out time {self.clock_out_at}"
                )

        if self.breaks:
            BreakInterval.validate_no_overlaps(self.breaks)

    def clock_in(self, time: DateTime) -> None:
        if self.state != AttendanceState.CLOCKED_OUT:
            raise InvalidStateTransitionError(
                f"Cannot clock in when state is {self.state.value}"
            )

        self.clock_in_at = time
        self.state = AttendanceState.CLOCKED_IN

    def start_break(self, time: DateTime) -> None:
        if self.state != AttendanceState.CLOCKED_IN:
            raise InvalidStateTransitionError(
                f"Cannot start break when state is {self.state.value}"
            )

        if self.clock_in_at and time <= self.clock_in_at:
            raise InvalidTimeRangeError(
                f"Break start time {time} must be after clock in time {self.clock_in_at}"
            )

        new_break = BreakInterval(start_at=time)
        self.breaks.append(new_break)
        self.state = AttendanceState.ON_BREAK

    def end_break(self, time: DateTime) -> None:
        if self.state != AttendanceState.ON_BREAK:
            raise InvalidStateTransitionError(
                f"Cannot end break when state is {self.state.value}"
            )

        ongoing_break = self._get_ongoing_break()
        if not ongoing_break:
            raise InvalidStateTransitionError("No ongoing break found")

        ongoing_break.end(time)
        BreakInterval.validate_no_overlaps(self.breaks)
        self.state = AttendanceState.CLOCKED_IN

    def clock_out(self, time: DateTime) -> None:
        if self.state != AttendanceState.CLOCKED_IN:
            raise InvalidStateTransitionError(
                f"Cannot clock out when state is {self.state.value}"
            )

        if self.clock_in_at and time <= self.clock_in_at:
            raise InvalidTimeRangeError(
                f"Clock out time {time} must be after clock in time {self.clock_in_at}"
            )

        for break_interval in self.breaks:
            if break_interval.end_at and break_interval.end_at >= time:
                raise InvalidTimeRangeError(
                    f"Clock out time {time} must be after all break end times"
                )

        self.clock_out_at = time
        self.state = AttendanceState.CLOCKED_OUT

    def _get_ongoing_break(self) -> BreakInterval | None:
        for break_interval in self.breaks:
            if break_interval.is_ongoing():
                return break_interval
        return None

    def calculate_worked_minutes(self) -> Minutes | None:
        if not self.clock_in_at or not self.clock_out_at:
            return None

        total_delta = self.clock_out_at.value - self.clock_in_at.value
        total_minutes = int(total_delta.total_seconds() // 60)

        break_minutes = 0
        for break_interval in self.breaks:
            if break_interval.end_at:
                duration = break_interval.duration_minutes()
                if duration:
                    break_minutes += duration.value

        return Minutes(total_minutes - break_minutes)

    def is_complete(self) -> bool:
        return (
            self.state == AttendanceState.CLOCKED_OUT and
            self.clock_in_at is not None and
            self.clock_out_at is not None
        )