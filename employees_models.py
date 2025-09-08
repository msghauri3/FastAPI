from pydantic import BaseModel
from typing import Optional
from datetime import date

class EmployeeBase(BaseModel):
    EmployeeID: str
    EmployeeName: Optional[str] = None
    CNIC: Optional[str] = None
    FatherName: Optional[str] = None
    DOB: Optional[str] = None
    MobileNo: Optional[str] = None
    Department: Optional[str] = None
    Designation: Optional[str] = None
    DateOfJoining: Optional[date] = None
    EmployeeStatus: Optional[str] = None
    ModifiedBy: Optional[str] = None
    ModifiedOn: Optional[str] = None
    Details: Optional[str] = None
    Project: Optional[str] = None
    CarryForwardLeaves: Optional[float] = None
    Year2022: Optional[float] = None
    Year2023: Optional[float] = None
    AdjustedAjusted: Optional[int] = None
    Year2024: Optional[int] = None
    CarryForwardLeaves1: Optional[float] = None
    Year2023New: Optional[float] = None
    BasicSalary: Optional[float] = None
    ApplyTax: Optional[str] = None

class EmployeeCreate(EmployeeBase):
    pass

class EmployeeUpdate(EmployeeBase):
    EmployeeID: Optional[str] = None

class Employee(EmployeeBase):
    uid: int
    
    class Config:
        from_attributes = True