from typing import Optional

from pydantic import BaseModel


# Shared properties
class RecordBase(BaseModel):
    zone: str
    owner: str
    rtype: str
    rdata: str
    ttl: int


# Properties to receive via API on creation
class RecordCreate(RecordBase):
    pass


# Properties to receive via API on update
class RecordUpdate(RecordBase):
    pass


class RecordInDBBase(RecordBase):
    id: Optional[int] = None


# Additional properties to return via API
class Record(RecordInDBBase):
    pass
