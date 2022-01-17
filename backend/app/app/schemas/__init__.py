from typing import Generic, List, Optional, TypeVar

from fastapi import FastAPI
from pydantic.generics import GenericModel

DataT = TypeVar("DataT")


class Response(GenericModel, Generic[DataT]):
    """Wrapper for responses"""

    data: Optional[DataT]
