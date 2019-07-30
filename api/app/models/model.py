from app import  db, psycopg2
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
        query = "SELECT * FROM {}".format(table)
        db.execute(query)
        rows = db.fetchall()
        retry_counter = 0
        for row in rows:
            results.append(dict(zip(column, row)))
    except (psycopg2.DatabaseError, psycopg2.OperationalError) as error:
        print(error)
        return retry_execute(query, column, retry_counter, error)
    else:
        return results

def get_by_id(table, field= None, value= None):
    column = get_columns(table)
    results = list()
    retry_counter = 0
    try:
        query = "SELECT * FROM "+table+" WHERE "+field+"='%s'" % str(value)
        db.execute(query)
        rows = db.fetchall()
        for row in rows:
            results.append(dict(zip(column, row)))
    except (psycopg2.DatabaseError, psycopg2.OperationalError) as error:
        print(error)
        return retry_execute(query, column, retry_counter, error)
    else:
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
        query = "INSERT INTO "+table+" "+column+" VALUES "+value+" RETURNING *"
        db.execute(query)
    except (Exception, psycopg2.DatabaseError) as e:
        raise e
    else:
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
        db.execute("UPDATE "+table+" SET "+set+" WHERE "+field+"="+data['where'][field]+"")
        status = True
    except (Exception, psycopg2.DatabaseError) as e:
        status = e
    finally:
        return status


def delete(table, field = None, value = None):
    rows_deleted = 0
    try:
        db.execute("DELETE FROM "+table+" WHERE "+field+" ="+value)
        rows_deleted = db.rowcount
    except (Exception, psycopg2.DatabaseError) as error:
        raise error
    else:
        return rows_deleted

def retry_execute(query, column, retry_counter, error):
    results = list()
    if retry_counter >= LIMIT_RETRIES:
        raise error
    else:
        retry_counter += 1
        print("got error {}. retrying {}".format(str(error).strip(), retry_counter))
        db.execute(query)
        rows = db.fetchall()
        for row in rows:
            results.append(dict(zip(column, row)))
        return results
