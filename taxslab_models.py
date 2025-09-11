from pydantic import BaseModel
from typing import Optional
from datetime import date

class TaxSlabBase(BaseModel):
    FiscalYearStart: Optional[date] = None
    FiscalYearEnd: Optional[date] = None
    LowerLimit: Optional[float] = None
    UpperLimit: Optional[float] = None
    TaxRate: Optional[float] = None

class TaxSlabCreate(TaxSlabBase):
    pass

class TaxSlabUpdate(TaxSlabBase):
    pass

class TaxSlab(TaxSlabBase):
    SlabID: int

    class Config:
        from_attributes = True
