from app import  db, conn, psycopg2
import json

LIMIT_RETRIES = 5

def get_columns(table):
    column = None
    try:
        query = "SELECT column_name FROM information_schema.columns WHERE table_schema = 'public' AND table_name='"+table+"'"
        db.execute(query)
        column = [row[0] for row in db.fetchall()]
    except (Exception, psycopg2.DatabaseError) as e:
        column = str(e)
    return column


def get_all(table):
    column = get_columns(table)
    results = list()
    try:
        query = "SELECT * FROM %s" % (table)
        db.execute(query)
        rows = db.fetchall()
        for row in rows:
            results.append(dict(zip(column, row)))
    except (psycopg2.DatabaseError, psycopg2.OperationalError) as error:
        conn.rollback()
        retry_counter = 0
        return retry_execute(query, column, retry_counter, error)
    else:
        conn.commit()
        return results

def get_by_id(table, field= None, value= None):
    column = get_columns(table)
    results = list()
    try:
        query = "SELECT * FROM %s WHERE %s='%s'" % (table, field, str(value))
        db.execute(query)
        rows = db.fetchall()
        for row in rows:
            results.append(dict(zip(column, row)))
    except (psycopg2.DatabaseError, psycopg2.OperationalError) as error:
        conn.rollback()
        retry_counter = 0
        return retry_execute(query, column, retry_counter, error)
    else:
        conn.commit()
        return results


def insert(table, data = None):
    value = ''
    column = ''
    for row in data:
        column += row+","
        value += "'%s'," % str(data[row])
    column = "("+column[:-1]+")"
    value = "("+value[:-1]+")"
    try:
        query = "INSERT INTO %s %s VALUES %s RETURNING *" % (table, column, value)
        db.execute(query)
    except (Exception, psycopg2.DatabaseError) as e:
        conn.rollback()
        raise e
    else:
        conn.commit()
        id_of_new_row = db.fetchone()[0]
        return str(id_of_new_row)

def update(table, data = None):
    value = ''
    rows = data['data']
    for row in rows:
        value += row+"='%s'," % str(rows[row])
    set = value[:-1]
    field = list(data['where'].keys())[0]
    status = None
    try:
        query = "UPDATE %s SET %s WHERE %s='%s'" % (table, set, field, data['where'][field])
        db.execute(query)
    except (Exception, psycopg2.DatabaseError) as e:
        conn.rollback()
        raise e
    else:
        conn.commit()
        status = True
        return status


def delete(table, field = None, value = None):
    rows_deleted = 0
    try:
        db.execute("DELETE FROM %s WHERE %s=%s" % (table, field, value))
    except (Exception, psycopg2.DatabaseError) as error:
        conn.rollback()
        raise error
    else:
        conn.commit()
        rows_deleted = db.rowcount
        return rows_deleted

def retry_execute(query, column, retry_counter, error):
    results = list()
    if retry_counter >= LIMIT_RETRIES:
        raise error
    else:
        retry_counter += 1
        print("got error {}. retrying {}".format(str(error).strip(), retry_counter))
        try:
            db.execute(query)
        except (Exception, psycopg2.DatabaseError) as error:
            conn.rollback()
        else:
            conn.commit()
            rows = db.fetchall()
            for row in rows:
                results.append(dict(zip(column, row)))
            return results
