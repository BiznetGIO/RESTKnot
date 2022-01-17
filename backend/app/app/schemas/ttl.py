from typing import Optional

from pydantic import BaseModel


# Shared properties
class TTLBase(BaseModel):
    ttl: Optional[int] = None


# Properties to receive via API on creation
class TTLCreate(TTLBase):
    ttl: int


# Properties to receive via API on update
class TTLUpdate(TTLBase):
    ttl: int


class TTLInDBBase(TTLBase):
    id: Optional[int] = None


# Additional properties to return via API
class TTL(TTLInDBBase):
    pass
