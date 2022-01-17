from typing import Any, List, Optional

from app.helpers import helpers
from app.models import connect


def get_all() -> List[Any]:
    cursor, _ = connect()

    query = """ SELECT * FROM "user" """
    cursor.execute(query, prepare=True)
    rows = cursor.fetchall()
    return rows


def get(user_id: int) -> Optional[Any]:
    cursor, _ = connect()

    query = f""" SELECT * FROM "user"  WHERE "id" = '{user_id}' """
    cursor.execute(query, prepare=True)
    row = cursor.fetchone()
    return row


def get_by_email(email: str) -> Optional[Any]:
    cursor, _ = connect()

    query = f""" SELECT * FROM "user"  WHERE "email" = '{email}' """
    cursor.execute(query, prepare=True)
    row = cursor.fetchone()
    return row


def add(email) -> Optional[Any]:
    cursor, connection = connect()

    created_at = helpers.get_datetime()
    query = f""" INSERT INTO "user" (email, created_at) VALUES ('{email}', '{created_at}') RETURNING *"""
    cursor.execute(query, prepare=True)
    connection.commit()

    user = cursor.fetchone()
    return user


def update(email, user_id) -> Optional[Any]:
    cursor, connection = connect()

    created_at = helpers.get_datetime()
    query = f""" UPDATE "user" SET "email" = '{email}', "created_at" =  '{created_at}' WHERE "id" = {user_id} RETURNING * """
    cursor.execute(query, prepare=True)
    connection.commit()

    user = cursor.fetchone()
    return user


def delete(user_id):
    cursor, connection = connect()

    query = f""" DELETE FROM "user" WHERE "id" = {user_id} RETURNING * """
    cursor.execute(query, prepare=True)
    connection.commit()
