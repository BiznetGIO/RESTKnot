from typing import Any

from fastapi import APIRouter

from app.schemas import health as schema
from app.schemas import Response

router = APIRouter()


@router.get("/", response_model=Response[schema.Health])
def check_health() -> Any:
    """
    Check server health.
    """
    status = {
        "status": "running",
    }
    return Response(data=status)
