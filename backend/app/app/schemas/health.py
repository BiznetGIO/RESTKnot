from pydantic import BaseModel


# Shared properties
class HealthBase(BaseModel):
    status: str = None


# Additional properties to return via API
class Health(HealthBase):
    pass
