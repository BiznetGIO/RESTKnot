from typing import Any, List

import logging

from fastapi import APIRouter, HTTPException
from pydantic.networks import EmailStr

from app.models import user as db
from app.schemas import Response
from app.schemas import user as schema

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/", response_model=Response[List[schema.User]])
def read_all() -> Any:
    """
    Retrieve users.
    """
    users = db.get_all()
    if not users:
        raise HTTPException(status_code=404, detail="user not found")

    return Response(data=users)


@router.get("/{user_id}", response_model=Response[schema.User])
def read(user_id: int) -> Any:
    """
    Get a specific user by id.
    """
    user = db.get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="user not found")

    return Response(data=user)


@router.get("/email/{email}", response_model=Response[schema.User])
def read_by_email(email: EmailStr) -> Any:
    """
    Get a specific user by id.
    """
    user = db.get_by_email(email)
    if not user:
        raise HTTPException(status_code=404, detail="user not found")

    return Response(data=user)


@router.post("/", response_model=Response[schema.User], status_code=201)
def create_user(user_in: schema.UserCreate) -> Any:
    """
    Create new user.
    """
    user = db.get_by_email(user_in.email)
    if user:
        raise HTTPException(
            status_code=409,
            detail="user with this email already exists",
        )

    user = db.add(user_in.email)
    return Response(data=user)


@router.put("/{user_id}", response_model=Response[schema.User])
def update(user_id: int, user_in: schema.UserCreate) -> Any:
    """
    Update the user.
    """
    user = db.get_by_email(user_in.email)
    if user:
        raise HTTPException(
            status_code=409,
            detail="user with this email already exists",
        )

    user = db.update(user_in.email, user_id)
    return Response(data=user)


@router.delete("/{user_id}", status_code=204)
def delete(user_id: int) -> Any:
    """
    Delete the user.
    """
    user = db.get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="user not found")

    db.delete(user_id)
