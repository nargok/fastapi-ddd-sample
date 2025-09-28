from abc import ABC, abstractmethod
from typing import Optional, List
from ..models import EmployeeId, RequestId, RequestStatus
from ..models.leave_request import LeaveRequest


class LeaveRequestRepository(ABC):

    @abstractmethod
    def find_by_id(self, request_id: RequestId) -> Optional[LeaveRequest]:
        """Find leave request by ID"""
        pass

    @abstractmethod
    def save(self, request: LeaveRequest) -> None:
        """Save or update leave request"""
        pass

    @abstractmethod
    def list_by_employee(
        self,
        employee_id: EmployeeId,
        status: Optional[RequestStatus] = None
    ) -> List[LeaveRequest]:
        """List leave requests by employee ID and optional status filter"""
        pass

    @abstractmethod
    def list_for_approver(
        self,
        approver_id: EmployeeId,
        status: Optional[RequestStatus] = None
    ) -> List[LeaveRequest]:
        """List leave requests for an approver with optional status filter"""
        pass