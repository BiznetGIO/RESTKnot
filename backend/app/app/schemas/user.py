from typing import Optional

from pydantic import BaseModel, EmailStr, Field


# Shared properties
class UserBase(BaseModel):
    email: Optional[EmailStr] = None


# Properties to receive via API on creation
class UserCreate(UserBase):
    email: EmailStr


# Properties to receive via API on update
class UserUpdate(UserBase):
    email: EmailStr


class UserInDBBase(UserBase):
    id: Optional[int] = None
    # created_at: Optional[str] = Field(..., exclude=True)


# Additional properties to return via API
class User(UserInDBBase):
    pass
