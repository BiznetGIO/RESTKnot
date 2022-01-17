from typing import Optional, List

from pydantic import BaseModel

from app.schemas import record as record_schema
from app.schemas import user as user_schema


# Shared properties
class DomainBase(BaseModel):
    zone: str
    user: Optional[user_schema.User]
    records: Optional[List[Optional[record_schema.Record]]]


# Properties to receive via API on creation
class DomainCreate(DomainBase):
    user_id: int


# Properties to receive via API on update
class DomainUpdate(DomainBase):
    pass


class DomainInDBBase(DomainBase):
    zone_id: Optional[int] = None


# Additional properties to return via API
class Domain(DomainInDBBase):
    pass
