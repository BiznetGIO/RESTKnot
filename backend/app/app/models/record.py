from typing import Any, List, Optional

from app.models import connect


def get_all() -> List[Any]:
    cursor, _ = connect()

    query = """ SELECT * FROM "record" """
    cursor.execute(query, prepare=True)
    rows = cursor.fetchall()
    return rows


def get(record_id: int) -> Optional[Any]:
    cursor, _ = connect()

    query = f""" SELECT * FROM "record"  WHERE "id" = '{record_id}' """
    cursor.execute(query, prepare=True)
    row = cursor.fetchone()
    return row


def get_by_zone_id(zone_id: int) -> List[Any]:
    cursor, _ = connect()

    query = f""" SELECT * FROM "record"  WHERE "zone_id" = '{zone_id}' """
    cursor.execute(query, prepare=True)
    row = cursor.fetchall()
    return row


def add(
    owner: str,
    rdata: str,
    zone_id: int,
    rtype_id: int,
    ttl_id: int,
) -> Optional[Any]:
    cursor, connection = connect()

    query = f""" INSERT INTO "record" (owner, rdata, zone_id, rtype_id, ttl_id) VALUES ('{owner}', '{rdata}', '{zone_id}', '{rtype_id}', '{ttl_id}') RETURNING *"""
    cursor.execute(query, prepare=True)
    connection.commit()

    record = cursor.fetchone()
    return record


def update(
    owner: str, rdata: str, zone_id: int, rtype_id: int, ttl_id: int, record_id: int
) -> Optional[Any]:
    cursor, connection = connect()

    query = f""" UPDATE "record" SET "owner" = '{owner}', "rdata" = '{rdata}', "zone_id" = {zone_id}, "rtype_id" = {rtype_id}, "ttl_id" = {ttl_id} WHERE "id" = {record_id} RETURNING *"""
    cursor.execute(query, prepare=True)
    connection.commit()

    record = cursor.fetchone()
    return record


def delete(record_id: int):
    cursor, connection = connect()

    query = f""" DELETE FROM "record" WHERE "id" = {record_id} RETURNING * """
    cursor.execute(query, prepare=True)
    connection.commit()
