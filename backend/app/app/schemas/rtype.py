from typing import Optional

from pydantic import BaseModel


# Shared properties
class RtypeBase(BaseModel):
    rtype: Optional[str] = None


# Properties to receive via API on creation
class RtypeCreate(RtypeBase):
    rtype: str


# Properties to receive via API on update
class RtypeUpdate(RtypeBase):
    rtype: str


class RtypeInDBBase(RtypeBase):
    id: Optional[str] = None


# Additional properties to return via API
class Rtype(RtypeInDBBase):
    pass
