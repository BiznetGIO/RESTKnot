from typing import Dict, List

from pydantic import BaseModel


# Additional properties to return via API
class MetaConfig(BaseModel):
    brokers: List[str] = None
    knot_servers: Dict = None


# Additional properties to return via API
class MetaVersion(BaseModel):
    build: str = None
