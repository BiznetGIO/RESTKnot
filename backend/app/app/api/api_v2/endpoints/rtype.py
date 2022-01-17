from typing import Any, List

from fastapi import APIRouter, HTTPException

from app.models import rtype as db
from app.schemas import rtype as schema

router = APIRouter()


@router.get("/", response_model=List[schema.Rtype])
def read_all() -> Any:
    """
    Retrieve ttls.
    """
    rtypes = db.get_all()
    return rtypes


@router.get("/{rtype_id}", response_model=schema.Rtype)
def read(rtype_id: int) -> Any:
    """
    Get a specific rtype by id.
    """
    rtype = db.get(rtype_id)
    if not rtype:
        raise HTTPException(status_code=404, detail="rtype not found")

    return rtype


@router.post("/", response_model=schema.Rtype, status_code=201)
def create_rtype(rtype_in: schema.RtypeCreate) -> Any:
    """
    Create new rtype.
    """
    rtype = db.get_by_value(rtype_in.rtype)
    if rtype:
        raise HTTPException(
            status_code=400,
            detail="rtype with this email already exists in the system",
        )

    rtype = db.add(rtype_in.rtype)
    return rtype


@router.put("/{rtype_id}", response_model=schema.Rtype)
def update(rtype_id: int, rtype_in: schema.RtypeCreate) -> Any:
    """
    Update the rtype.
    """
    rtype = db.get_by_value(rtype_in.rtype)
    if rtype:
        raise HTTPException(
            status_code=400,
            detail="rtype with this value already exists in the system",
        )

    rtype = db.update(rtype_in.rtype, rtype_id)
    return rtype


@router.delete("/{rtype_id}", status_code=204)
def delete(rtype_id: int) -> Any:
    """
    Delete the rtype.
    """
    rtype = db.get(rtype_id)
    if not rtype:
        raise HTTPException(status_code=404, detail="rtype not found")

    db.delete(rtype_id)
