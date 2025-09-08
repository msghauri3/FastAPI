from pydantic import BaseModel
from typing import Optional
from datetime import date

class EmployeeLeaveBase(BaseModel):
    EmployeeID: str
    LeaveTypeName: str
    StartDate: date
    EndDate: date
    TotalDays: Optional[float] = None
    AddDays: Optional[int] = None
    ExcludeDays: Optional[int] = None
    Short_Adj: Optional[str] = None
    DepSupervisorComments: Optional[str] = None
    Year: Optional[str] = None
    Status: Optional[str] = None
    ApprovedBy: Optional[str] = None
    ApprovedOn: Optional[date] = None
    AppliedDate: Optional[date] = None

class EmployeeLeaveCreate(EmployeeLeaveBase):
    pass

class EmployeeLeaveUpdate(EmployeeLeaveBase):
    EmployeeID: Optional[str] = None
    LeaveTypeName: Optional[str] = None
    StartDate: Optional[date] = None
    EndDate: Optional[date] = None

class EmployeeLeave(EmployeeLeaveBase):
    uid: int
    
    class Config:
        from_attributes = True