from pydantic import BaseModel
from typing import Optional

class AllowanceBase(BaseModel):
    EmployeeID: Optional[str] = None
    AllowanceType: Optional[str] = None
    Amount: Optional[float] = None
    IsActive: Optional[str] = None
    Frequency: Optional[str] = None

class AllowanceCreate(AllowanceBase):
    EmployeeID: str
    AllowanceType: str
    Amount: float

class AllowanceUpdate(AllowanceBase):
    pass

class Allowance(AllowanceBase):
    AllowanceID: int

    class Config:
        from_attributes = True
