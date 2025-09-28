from dataclasses import dataclass
from .value_objects import EmployeeId, EmploymentType


@dataclass
class Employee:
    employee_id: EmployeeId
    name: str
    employment_type: EmploymentType

    def __post_init__(self):
        if not self.employee_id:
            raise ValueError("Employee ID is required")
        if not self.name or not self.name.strip():
            raise ValueError("Employee name is required")
        if not isinstance(self.employment_type, EmploymentType):
            raise ValueError("Invalid employment type")