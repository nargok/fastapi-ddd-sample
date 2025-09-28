from dataclasses import dataclass
import uuid
from ..models.value_objects import (
    RequestId,
    EmployeeId,
    DateRange,
    LeaveType,
    RequestStatus
)
from ..exceptions import InvalidStateTransitionError


@dataclass
class LeaveRequest:
    request_id: RequestId
    employee_id: EmployeeId
    date_range: DateRange
    leave_type: LeaveType
    reason: str
    status: RequestStatus = RequestStatus.PENDING
    reviewer_id: EmployeeId | None = None
    review_comment: str | None = None

    def __post_init__(self):
        if not self.request_id:
            self.request_id = RequestId(str(uuid.uuid4()))

        if not self.employee_id:
            raise ValueError("Employee ID is required")

        if not self.date_range:
            raise ValueError("Date range is required")

        if not isinstance(self.leave_type, LeaveType):
            raise ValueError("Invalid leave type")

        if not self.reason or not self.reason.strip():
            raise ValueError("Reason is required")

    def approve(self, approver_id: EmployeeId, comment: str | None = None) -> None:
        if self.status != RequestStatus.PENDING:
            raise InvalidStateTransitionError(
                f"Cannot approve request with status {self.status.value}"
            )
        self.status = RequestStatus.APPROVED
        self.reviewer_id = approver_id
        self.review_comment = comment

    def reject(self, approver_id: EmployeeId, comment: str | None = None) -> None:
        if self.status != RequestStatus.PENDING:
            raise InvalidStateTransitionError(
                f"Cannot reject request with status {self.status.value}"
            )
        self.status = RequestStatus.REJECTED
        self.reviewer_id = approver_id
        self.review_comment = comment

    def is_pending(self) -> bool:
        return self.status == RequestStatus.PENDING