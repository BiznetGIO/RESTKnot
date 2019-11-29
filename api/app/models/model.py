import psycopg2

from app import database
from app.models.prepare import PreparingCursor


def get_db():
    try:
        connection = database.connect()
        cursor = connection.cursor(cursor_factory=PreparingCursor)
        return cursor, connection
    except Exception as exc:
        raise ValueError(f"{exc}")


def get_columns(table):
    column = None
    cursor, connection = get_db()
    try:
        query = f"SELECT column_name FROM information_schema.columns WHERE table_schema = 'public' AND table_name='{table}'"
        cursor.execute(query)
        column = [row[0] for row in cursor.fetchall()]
        return column
    except (Exception, psycopg2.DatabaseError) as e:
        column = str(e)
    finally:
        if connection:
            cursor.close()
            connection.close()


def get_all(table):
    results = []
    column = get_columns(table)
    cursor, connection = get_db()
    try:
        query = f'SELECT * FROM "{table}"'
        cursor.prepare(query)
        cursor.execute()
        rows = cursor.fetchall()
        for row in rows:
            results.append(dict(zip(column, row)))
    except (psycopg2.DatabaseError, psycopg2.OperationalError) as error:
        connection.rollback()
        raise error
    else:
        # even select need `commit`
        # see /psycopg/docs/faq.html#problems-with-transactions-handling
        connection.commit()
        return results
    finally:
        if connection:
            cursor.close()
            connection.close()


def get_by_condition(table, field=None, value=None):
    results = []
    cursor, connection = get_db()
    column = get_columns(table)
    try:
        query = f'SELECT * FROM "{table}" WHERE "{field}"=%(value)s'
        cursor.prepare(query)
        cursor.execute({"value": value})
        rows = cursor.fetchall()
        for row in rows:
            results.append(dict(zip(column, row)))
    except (psycopg2.DatabaseError, psycopg2.OperationalError) as error:
        connection.rollback()
        raise error
    else:
        connection.commit()
        return results
    finally:
        if connection:
            cursor.close()
            connection.close()


def insert(table, data=None):
    cursor, connection = get_db()
    value = ""
    column = ""
    str_placeholer = ""

    # arrange column and values
    for row in data:
        column += row + ","
        value += f"{data[row]},"
        str_placeholer += "%s,"
    column = column[:-1]
    value = value[:-1]
    str_placeholer = str_placeholer[:-1]

    try:
        query = (
            f'INSERT INTO "{table}" ({column}) VALUES ({str_placeholer}) RETURNING *'
        )
        value_as_tuple = tuple(value.split(","))
        cursor.prepare(query)
        cursor.execute((value_as_tuple))
    except (Exception, psycopg2.DatabaseError) as e:
        connection.rollback()
        raise e
    else:
        connection.commit()
        id_of_new_row = cursor.fetchone()[0]
        return str(id_of_new_row)
    finally:
        if connection:
            cursor.close()
            connection.close()


def update(table, data=None):
    cursor, connection = get_db()
    value = ""
    rows = data["data"]
    for row in rows:
        value += row + "='%s'," % str(rows[row])
    _set = value[:-1]
    field = list(data["where"].keys())[0]
    status = None
    try:
        field_data = data["where"][field]
        query = f'UPDATE "{table}" SET {_set} WHERE {field}=%(field_data)s'
        cursor.prepare(query)
        cursor.execute({"field_data": field_data})
    except (Exception, psycopg2.DatabaseError) as e:
        connection.rollback()
        raise e
    else:
        connection.commit()
        status = True
        return status
    finally:
        if connection:
            cursor.close()
            connection.close()


def delete(table, field=None, value=None):
    cursor, connection = get_db()
    rows_deleted = 0
    try:
        query = f'DELETE FROM "{table}" WHERE {field}=%(value)s'
        cursor.prepare(query)
        cursor.execute({"value": value})
    except (Exception, psycopg2.DatabaseError) as error:
        connection.rollback()
        raise error
    else:
        connection.commit()
        rows_deleted = cursor.rowcount
        return str(rows_deleted)
    finally:
        if connection:
            cursor.close()
            connection.close()


def is_unique(table, field=None, value=None):
    unique = True
    data = get_by_condition(table=table, field=field, value=value)

    if data:  # initial database will return None
        if len(data) != 0:
            unique = False

    return unique


def plain_get(query, value=None):
    results = []
    cursor, connection = get_db()
    try:
        cursor.prepare(query)
        cursor.execute(value)
        results = cursor.fetchall()
    except (psycopg2.DatabaseError, psycopg2.OperationalError) as error:
        connection.rollback()
        raise error
    else:
        connection.commit()
        return results
    finally:
        if connection:
            cursor.close()
            connection.close()
