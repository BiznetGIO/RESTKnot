from typing import Any, Dict, List, Optional

from app.models import connect


def get_all() -> List[Any]:
    cursor, _ = connect()

    query = """ SELECT * FROM "zone" """
    cursor.execute(query, prepare=True)
    rows = cursor.fetchall()
    return rows


def get(zone_id: int) -> Optional[Any]:
    cursor, _ = connect()

    query = f""" SELECT * FROM "zone"  WHERE "id" = '{zone_id}' """
    cursor.execute(query, prepare=True)
    row = cursor.fetchone()
    return row


def get_by_name(zone_name: str) -> Optional[Any]:
    cursor, _ = connect()

    query = f""" SELECT * FROM "zone"  WHERE "zone" = '{zone_name}' """
    cursor.execute(query, prepare=True)
    rows = cursor.fetchone()
    return rows


def get_by_user_id(user_id: int) -> List[Dict]:
    cursor, _ = connect()

    query = f""" SELECT * FROM "zone"  WHERE "user_id" = '{user_id}' """
    cursor.execute(query, prepare=True)
    rows = cursor.fetchall()
    return rows


def add(zone_name: str, user_id: int) -> Optional[Any]:
    cursor, connection = connect()

    query = f""" INSERT INTO "zone" (zone, user_id) VALUES ('{zone_name}', '{user_id}') RETURNING *"""
    cursor.execute(query, prepare=True)
    connection.commit()

    zone = cursor.fetchone()
    return zone


def delete(zone_id: int):
    cursor, connection = connect()

    query = f""" DELETE FROM "zone" WHERE "id" = {zone_id} RETURNING * """
    cursor.execute(query, prepare=True)
    connection.commit()
