from pydantic import BaseModel
from typing import Optional
from datetime import date

class PromotionBase(BaseModel):
    EmployeeID: Optional[str] = None
    Title: Optional[str] = None
    EffectiveDate: Optional[date] = None
    NewSalary: Optional[float] = None
    Remarks: Optional[str] = None

class PromotionCreate(PromotionBase):
    pass

class PromotionUpdate(BaseModel):
    EmployeeID: Optional[str] = None
    Title: Optional[str] = None
    EffectiveDate: Optional[date] = None
    NewSalary: Optional[float] = None
    Remarks: Optional[str] = None

class Promotion(PromotionBase):
    PromotionID: int  # ✅ Primary Key

    class Config:
        from_attributes = True
