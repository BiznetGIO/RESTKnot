from typing import Any

from fastapi import APIRouter

from app.helpers import helpers
from app.schemas import meta as schema
from app.schemas import Response

router = APIRouter()


@router.get("/config", response_model=Response[schema.MetaConfig])
def read_config() -> Any:
    """
    Get server configuration.
    """
    config = helpers.get_config()
    brokers = config["brokers"]
    clusters = config["knot_servers"]

    result = {"knot_servers": clusters, "brokers": brokers}
    return Response(data=result)


@router.get("/version", response_model=Response[schema.MetaVersion])
def read_version() -> Any:
    """
    Get server version.
    """
    version = helpers.app_version()

    result = {"build": version["vcs_revision"]}
    return Response(data=result)
