from typing import Any, List, Optional

from app.models import connect


def get_all() -> List[Any]:
    cursor, _ = connect()

    query = """ SELECT * FROM "ttl" """
    cursor.execute(query, prepare=True)
    rows = cursor.fetchall()
    return rows


def get(ttl_id: int) -> Optional[Any]:
    cursor, _ = connect()

    query = f""" SELECT * FROM "ttl"  WHERE "id" = '{ttl_id}' """
    cursor.execute(query, prepare=True)
    row = cursor.fetchone()
    return row


def get_by_value(ttl: str) -> Optional[Any]:
    cursor, _ = connect()

    query = f""" SELECT * FROM "ttl"  WHERE "ttl" = '{ttl}' """
    cursor.execute(query, prepare=True)
    row = cursor.fetchone()
    return row


def add(ttl: str) -> Optional[Any]:
    cursor, connection = connect()

    query = f""" INSERT INTO "ttl" (ttl) VALUES ('{ttl}') RETURNING *"""
    cursor.execute(query, prepare=True)
    connection.commit()

    _ttl = cursor.fetchone()
    return _ttl


def update(ttl: str, ttl_id: int) -> Optional[Any]:
    cursor, connection = connect()

    query = f""" UPDATE "ttl" SET "ttl" = '{ttl}' WHERE "id" = {ttl_id} RETURNING * """
    cursor.execute(query, prepare=True)
    connection.commit()

    _ttl = cursor.fetchone()
    return _ttl


def delete(ttl_id: int):
    cursor, connection = connect()

    query = f""" DELETE FROM "ttl" WHERE "id" = {ttl_id} RETURNING * """
    cursor.execute(query, prepare=True)
    connection.commit()
