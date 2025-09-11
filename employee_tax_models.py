from pydantic import BaseModel
from typing import Optional

class EmployeeTaxBase(BaseModel):
    EmployeeID: Optional[str] = None
    SalaryYear: Optional[int] = None
    SalaryMonth: Optional[str] = None
    SlabID: Optional[int] = None
    TaxAmount: Optional[float] = None

class EmployeeTaxCreate(EmployeeTaxBase):
    pass

class EmployeeTaxUpdate(EmployeeTaxBase):
    pass

class EmployeeTax(EmployeeTaxBase):
    TaxID: int   # ✅ Primary key

    class Config:
        from_attributes = True
