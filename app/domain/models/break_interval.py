from dataclasses import dataclass
from typing import List
from ..exceptions import OverlappingBreaksError, InvalidTimeRangeError
from .value_objects import DateTime, Minutes


@dataclass
class BreakInterval:
    start_at: DateTime
    end_at: DateTime | None = None

    def __post_init__(self):
        if self.end_at and self.start_at >= self.end_at:
            raise InvalidTimeRangeError(
                f"Break start time {self.start_at} must be before end time {self.end_at}"
            )

    def is_ongoing(self) -> bool:
        return self.end_at is None

    def end(self, end_time: DateTime) -> None:
        if not self.is_ongoing():
            raise InvalidTimeRangeError("Break has already ended")
        if end_time <= self.start_at:
            raise InvalidTimeRangeError(
                f"Break end time {end_time} must be after start time {self.start_at}"
            )
        self.end_at = end_time

    def duration_minutes(self) -> Minutes | None:
        if self.end_at is None:
            return None
        delta = self.end_at.value - self.start_at.value
        return Minutes(int(delta.total_seconds() // 60))

    def overlaps_with(self, other: "BreakInterval") -> bool:
        if self.end_at is None or other.end_at is None:
            return True

        return not (
            self.end_at <= other.start_at or
            other.end_at <= self.start_at
        )

    @staticmethod
    def validate_no_overlaps(breaks: List["BreakInterval"]) -> None:
        for i, break1 in enumerate(breaks):
            for break2 in breaks[i + 1:]:
                if break1.overlaps_with(break2):
                    raise OverlappingBreaksError(
                        f"Break {break1} overlaps with {break2}"
                    )