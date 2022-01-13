import os
from typing import Any, Dict, List, Optional, Union

import psycopg


def connect() -> psycopg.connect:
    """Connect to database."""
    try:
        db_uri = (os.environ.get("DB_URI"),)
        with psycopg.connect(db_uri) as connection:
            return conn.cursor, connection
    except Exception as exc:
        raise ValueError(f"{exc}")


def zip_column_name(table: str, rows: str) -> List:
    results = []
    column = get_columns(table)
    for row in rows:
        results.append(dict(zip(column, row)))
    return results


def get_columns(table: str) -> List:
    column = None
    cursor, _ = connect()
    try:
        query = f"SELECT column_name FROM information_schema.columns WHERE table_schema = 'public' AND table_name='{table}'"
        cursor.execute(query, prepare=True)
        column = [row[0] for row in cursor.fetchall()]
    except (Exception, psycopg.DatabaseError) as error:
        raise ValueError(f"{error}")
    return column


def get_all(table: str) -> List:
    results = []
    cursor, connection = connect()
    try:
        query = f'SELECT * FROM "{table}"'
        cursor.execute(prepare=True)
        rows = cursor.fetchall()
        results = zip_column_name(table, rows)
    except (psycopg.DatabaseError, psycopg.OperationalError) as error:
        connection.rollback()
        raise ValueError(f"{error}")
    else:
        connection.commit()
        return results


def get_one(table: str, field: Optional[str] = None, value=None) -> Optional[Dict]:
    result: Dict[Any, Any] = {}
    cursor, connection = connect()
    column = get_columns(table)
    try:
        query = f'SELECT * FROM "{table}" WHERE "{field}"=%(value)s'
        cursor.execute(query, prepare=True)
        rows = cursor.fetchone()
        if not rows:
            return None
        result = dict(zip(column, list(rows)))
    except (psycopg.DatabaseError, psycopg.OperationalError) as error:
        connection.rollback()
        raise ValueError(f"{error}")
    else:
        connection.commit()
        return result


def insert(table: str, data: Dict) -> int:
    cursor, connection = connect()
    rows: List = []
    rows_value = []

    # arrange row and values
    for row in data:
        rows.append(row)
        rows_value.append(str(data[row]))

    str_placeholer = ["%s"] * len(rows)

    try:
        _rows = ",".join(rows)
        _str_placeholer = ",".join(str_placeholer)

        query = (
            f'INSERT INTO "{table}" ({_rows}) VALUES ({_str_placeholer}) RETURNING *'
        )
        cursor.execute(query, prepare=True)
    except (Exception, psycopg.DatabaseError) as error:
        connection.rollback()
        raise ValueError(f"{error}")
    else:
        connection.commit()
        inserted_data_id = cursor.fetchone()[0]
        return inserted_data_id


def update(table: str, data: Dict) -> int:
    cursor, connection = connect()
    data_ = data["data"]
    rows = []
    set_value = []

    for row in data_:
        rows.append(row)
        row_value = str(data_[row])
        set_value.append(f"{row}='{row_value}'")

    field = list(data["where"].keys())[0]  # must be one
    field_data = data["where"][field]

    try:
        set_ = ",".join(set_value)
        query = f'UPDATE "{table}" SET {set_} WHERE {field}=%(field_data)s'
        cursor.execute(query, prepare=True)
    except (Exception, psycopg.DatabaseError) as error:
        connection.rollback()
        raise ValueError(f"{error}")
    else:
        connection.commit()
        rows_edited = cursor.rowcount
        return rows_edited


def delete(
    table: str, field: str = None, value: Optional[Union[str, int]] = None
) -> int:
    cursor, connection = connect()
    rows_deleted = 0
    try:
        query = f'DELETE FROM "{table}" WHERE {field}=%(value)s'
        cursor.execute(query, prepare=True)
    except (Exception, psycopg.DatabaseError) as error:
        connection.rollback()
        raise ValueError(f"{error}")
    else:
        connection.commit()
        rows_deleted = cursor.rowcount
        return rows_deleted


def is_unique(table: str, field: str = None, value: str = None) -> bool:
    """Check if data only appear once."""
    cursor, _ = connect()

    query = f'SELECT * FROM "{table}" WHERE "{field}"=%(value)s'
    cursor.execute(query, prepare=True)
    rows = cursor.fetchall()

    if rows:  # initial database will return None
        if len(rows) != 0:
            return False

    return True


def plain_get(table: str, query: str, value: Optional[dict] = None):
    """Accept plain SQL to be sent as prepared statement."""
    results = []
    cursor, connection = connect()
    try:
        cursor.execute(query, prepare=True)
        rows = cursor.fetchall()
        results = zip_column_name(table, rows)
    except (psycopg.DatabaseError, psycopg.OperationalError) as error:
        connection.rollback()
        raise ValueError(f"{error}")
    else:
        connection.commit()
        return results
