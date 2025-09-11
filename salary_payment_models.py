from pydantic import BaseModel
from typing import Optional
from datetime import date

class SalaryPaymentBase(BaseModel):
    EmployeeID: Optional[str] = None
    SalaryYear: Optional[int] = None
    SalaryMonth: Optional[str] = None
    BasicSalary: Optional[float] = None
    TotalAllowances: Optional[float] = None
    TotalDeductions: Optional[float] = None
    TaxAmount: Optional[float] = None
    PaymentDate: Optional[date] = None
    SlabID: Optional[int] = None
    GrossSalary: Optional[float] = None

class SalaryPaymentCreate(SalaryPaymentBase):
    EmployeeID: str
    SalaryYear: int
    SalaryMonth: str
    BasicSalary: float

class SalaryPaymentUpdate(SalaryPaymentBase):
    pass

class SalaryPayment(SalaryPaymentBase):
    PaymentID: int
    NetSalary: Optional[float] = None  # computed column

    class Config:
        from_attributes = True
