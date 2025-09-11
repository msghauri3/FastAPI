from pydantic import BaseModel
from typing import Optional

class ConfigurationBase(BaseModel):
    ConfigKey: Optional[str] = None
    ConfigValue: Optional[str] = None

class ConfigurationCreate(ConfigurationBase):
    ConfigKey: str
    ConfigValue: str

class ConfigurationUpdate(ConfigurationBase):
    pass

class Configuration(ConfigurationBase):
    UID: int

    class Config:
        from_attributes = True
