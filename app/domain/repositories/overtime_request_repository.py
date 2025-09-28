from abc import ABC, abstractmethod
from typing import Optional, List
from ..models import EmployeeId, RequestId, RequestStatus
from ..models.overtime_request import OvertimeRequest


class OvertimeRequestRepository(ABC):

    @abstractmethod
    def find_by_id(self, request_id: RequestId) -> Optional[OvertimeRequest]:
        """Find overtime request by ID"""
        pass

    @abstractmethod
    def save(self, request: OvertimeRequest) -> None:
        """Save or update overtime request"""
        pass

    @abstractmethod
    def list_by_employee(
        self,
        employee_id: EmployeeId,
        status: Optional[RequestStatus] = None
    ) -> List[OvertimeRequest]:
        """List overtime requests by employee ID and optional status filter"""
        pass

    @abstractmethod
    def list_for_approver(
        self,
        approver_id: EmployeeId,
        status: Optional[RequestStatus] = None
    ) -> List[OvertimeRequest]:
        """List overtime requests for an approver with optional status filter"""
        pass