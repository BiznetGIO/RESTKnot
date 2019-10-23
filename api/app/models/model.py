import psycopg2

from app import database


def get_db():
    try:
        connection = database.connect()
        cursor = connection.cursor()
        return cursor, connection
    except Exception as exc:
        raise ValueError(f"{exc}")


def get_columns(table):
    column = None
    cursor, _ = get_db()
    try:
        query = f"SELECT column_name FROM information_schema.columns WHERE table_schema = 'public' AND table_name='{table}'"
        cursor.execute(query)
        column = [row[0] for row in cursor.fetchall()]
    except (Exception, psycopg2.DatabaseError) as e:
        column = str(e)
    return column


def get_all(table):
    results = []
    column = get_columns(table)
    cursor, connection = get_db()
    try:
        query = f'SELECT * FROM "{table}"'
        cursor.execute(query)
        rows = cursor.fetchall()
        for row in rows:
            results.append(dict(zip(column, row)))
    except (psycopg2.DatabaseError, psycopg2.OperationalError) as error:
        connection.rollback()
        retry_counter = 0
        return retry_execute(query, column, retry_counter, error)
    else:
        connection.commit()
        return results


# todo id_ value
def get_by_id(table, field=None, id_=None):
    results = []
    cursor, connection = get_db()
    column = get_columns(table)
    try:
        query = f'SELECT * FROM "{table}" WHERE "{field}"={id_}'
        print(query)
        cursor.execute(query)
        rows = cursor.fetchall()
        for row in rows:
            results.append(dict(zip(column, row)))
    except (psycopg2.DatabaseError, psycopg2.OperationalError) as error:
        connection.rollback()
        retry_counter = 0
        return retry_execute(query, column, retry_counter, error)
    else:
        connection.commit()
        return results


def insert(table, data=None):
    cursor, connection = get_db()
    value = ""
    column = ""

    # arrange column and values
    for row in data:
        column += row + ","
        value += f"'{data[row]}',"
    column = column[:-1]
    value = value[:-1]

    try:
        query = f'INSERT INTO "{table}" ({column}) VALUES ({value}) RETURNING *'
        cursor.execute(query)
    except (Exception, psycopg2.DatabaseError) as e:
        connection.rollback()
        raise e
    else:
        connection.commit()
        id_of_new_row = cursor.fetchone()[0]
        return str(id_of_new_row)


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
        query = f'UPDATE "{table}" SET {_set} WHERE {field}={field_data}'
        cursor.execute(query)
    except (Exception, psycopg2.DatabaseError) as e:
        connection.rollback()
        raise e
    else:
        connection.commit()
        status = True
        return status


def delete(table, field=None, value=None):
    cursor, connection = get_db()
    rows_deleted = 0
    try:
        query = f'DELETE FROM "{table}" WHERE {field}={value}'
        cursor.execute(query)
    except (Exception, psycopg2.DatabaseError) as error:
        connection.rollback()
        raise error
    else:
        connection.commit()
        rows_deleted = cursor.rowcount
        return str(rows_deleted)


def retry_execute(query, column, retry_counter, error):
    limit_retries = 5
    results = []
    cursor, connection = get_db()
    if retry_counter >= limit_retries:
        raise error
    else:
        retry_counter += 1
        print("got error {}. retrying {}".format(str(error).strip(), retry_counter))
        try:
            cursor.execute(query)
        except (Exception, psycopg2.DatabaseError):
            connection.rollback()
        else:
            connection.commit()
            rows = cursor.fetchall()
            for row in rows:
                results.append(dict(zip(column, row)))
            return results


def content_by_record(record):
    data = list()
    try:
        content_data = get_all("content")
    except Exception as e:
        raise e
    else:
        for i in content_data:
            if i["record"] == record:
                data.append(i)
    return data


def serial_by_record(record):
    result = list()
    try:
        content_data = get_all("serial")
    except Exception as e:
        raise e
    else:
        for i in content_data:
            if i["record"] == record:
                result.append(i)
    return result


def is_unique(table, field=None, value=None):
    unique = True
    data = get_by_id(table=table, field=field, id_=value)
    if len(data) != 0:
        unique = False
    return unique
