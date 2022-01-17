from typing import Any, List, Optional

from app.models import connect


def get_all() -> List[Any]:
    cursor, _ = connect()

    query = """ SELECT * FROM "rtype" """
    cursor.execute(query, prepare=True)
    rows = cursor.fetchall()
    return rows


def get(rtype_id: int) -> Optional[Any]:
    cursor, _ = connect()

    query = f""" SELECT * FROM "rtype"  WHERE "id" = '{rtype_id}' """
    cursor.execute(query, prepare=True)
    row = cursor.fetchone()
    return row


def get_by_value(rtype: str) -> Optional[Any]:
    cursor, _ = connect()

    query = f""" SELECT * FROM "rtype"  WHERE "rtype" = '{rtype}' """
    cursor.execute(query, prepare=True)
    row = cursor.fetchone()
    return row


def add(rtype: str) -> Optional[Any]:
    cursor, connection = connect()

    query = f""" INSERT INTO "rtype" (rtype) VALUES ('{rtype}') RETURNING *"""
    cursor.execute(query, prepare=True)
    connection.commit()

    rtype = cursor.fetchone()
    return rtype


def update(rtype: str, rtype_id: int) -> Optional[Any]:
    cursor, connection = connect()

    query = f""" UPDATE "rtype" SET "rtype" = '{rtype}' WHERE "id" = {rtype_id} RETURNING * """
    cursor.execute(query, prepare=True)
    connection.commit()

    rtype = cursor.fetchone()
    return rtype


def delete(rtype_id: int):
    cursor, connection = connect()

    query = f""" DELETE FROM "rtype" WHERE "id" = {rtype_id} RETURNING * """
    cursor.execute(query, prepare=True)
    connection.commit()
