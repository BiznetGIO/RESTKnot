from typing import Any, List

from fastapi import APIRouter, HTTPException

from app.models import ttl as db
from app.schemas import ttl as schema

router = APIRouter()


@router.get("/", response_model=List[schema.TTL])
def read_all() -> Any:
    """
    Retrieve ttls.
    """
    ttls = db.get_all()
    return ttls


@router.get("/{ttl_id}", response_model=schema.TTL)
def read(ttl_id: int) -> Any:
    """
    Get a specific ttl by id.
    """
    ttl = db.get(ttl_id)
    if not ttl:
        raise HTTPException(status_code=404, detail="ttl not found")

    return ttl


@router.post("/", response_model=schema.TTL, status_code=201)
def create_ttl(ttl_in: schema.TTLCreate) -> Any:
    """
    Create new ttl.
    """
    ttl = db.get_by_value(ttl_in.ttl)
    if ttl:
        raise HTTPException(
            status_code=400,
            detail="ttl with this email already exists in the system",
        )

    ttl = db.add(ttl_in.ttl)
    return ttl


@router.put("/{ttl_id}", response_model=schema.TTL)
def update(ttl_id: int, ttl_in: schema.TTLCreate) -> Any:
    """
    Update the ttl.
    """
    ttl = db.get_by_value(ttl_in.ttl)
    if ttl:
        raise HTTPException(
            status_code=400,
            detail="ttl with this value already exists in the system",
        )

    ttl = db.update(ttl_in.ttl, ttl_id)
    return ttl


@router.delete("/{ttl_id}", status_code=204)
def delete(ttl_id: int) -> Any:
    """
    Delete the ttl.
    """
    ttl = db.get(ttl_id)
    if not ttl:
        raise HTTPException(status_code=404, detail="ttl not found")

    db.delete(ttl_id)
