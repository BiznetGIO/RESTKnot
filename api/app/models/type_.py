from typing import Any, List, Optional

from app.models import connect


def get_all() -> List[Any]:
    cursor, _ = connect()

    query = """ SELECT * FROM "type" """
    cursor.execute(query, prepare=True)
    rows = cursor.fetchall()
    return rows


def get(type_id: int) -> Optional[Any]:
    cursor, _ = connect()

    query = f""" SELECT * FROM "type"  WHERE "id" = '{type_id}' """
    cursor.execute(query, prepare=True)
    row = cursor.fetchone()
    return row


def get_by_value(type_: str) -> Optional[Any]:
    cursor, _ = connect()

    query = f""" SELECT * FROM "type"  WHERE "type" = '{type_}' """
    cursor.execute(query, prepare=True)
    row = cursor.fetchone()
    return row


def add(type_: str) -> Optional[Any]:
    cursor, connection = connect()

    query = f""" INSERT INTO "type" (type) VALUES ('{type_}') RETURNING *"""
    cursor.execute(query, prepare=True)
    connection.commit()

    _type = cursor.fetchone()
    return _type


def update(type_: str, type_id: int) -> Optional[Any]:
    cursor, connection = connect()

    query = (
        f""" UPDATE "type" SET "type" = '{type_}' WHERE "id" = {type_id} RETURNING * """
    )
    cursor.execute(query, prepare=True)
    connection.commit()

    _type = cursor.fetchone()
    return _type


def delete(type_id: int):
    cursor, connection = connect()

    query = f""" DELETE FROM "type" WHERE "id" = {type_id} RETURNING * """
    cursor.execute(query, prepare=True)
    connection.commit()
