from pydantic import BaseModel
from typing import Optional

class EmployeeLeaveSummaryBase(BaseModel):
    EmployeeID: Optional[int] = None
    TotalYear2022: Optional[int] = None
    RemainingYear2022: Optional[int] = None
    TotalYear2023: Optional[int] = None
    RemainingYear2023: Optional[int] = None
    TotalYear2024: Optional[int] = None
    RemainingYear2024: Optional[int] = None
    TotalAllYears: Optional[int] = None
    RemainingAllYears: Optional[int] = None

class EmployeeLeaveSummaryCreate(EmployeeLeaveSummaryBase):
    pass

class EmployeeLeaveSummaryUpdate(EmployeeLeaveSummaryBase):
    pass

class EmployeeLeaveSummary(EmployeeLeaveSummaryBase):
    class Config:
        from_attributes = True
