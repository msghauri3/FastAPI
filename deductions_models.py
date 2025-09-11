from pydantic import BaseModel
from typing import Optional

class DeductionBase(BaseModel):
    EmployeeID: Optional[str] = None
    DeductionType: Optional[str] = None
    Amount: Optional[float] = None
    IsActive: Optional[str] = None
    Frequency: Optional[str] = None

class DeductionCreate(DeductionBase):
    EmployeeID: str
    DeductionType: str
    Amount: float

class DeductionUpdate(DeductionBase):
    pass

class Deduction(DeductionBase):
    DeductionID: int

    class Config:
        from_attributes = True
