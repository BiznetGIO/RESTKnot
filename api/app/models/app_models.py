from app import influx
from datetime import datetime


def create_db(dbname):
    return influx.create_database(dbname)

def timeset():
    return datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')

def use_db(dbname):
    influx.switch_database(database=dbname)
    return influx.switch_database(database=dbname)

def insert(dbname, data):
    return influx.write_points(data, database=dbname)

def delete(dbname=None,measurement=None, tags=None):
    return influx.delete_series(database=dbname, measurement=measurement, tags=tags)

def query(dbname,q):
    influx.switch_database(database=dbname)
    return influx.query(q)