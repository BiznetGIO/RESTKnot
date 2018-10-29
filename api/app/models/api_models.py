from . import app_models as db
import os


dbname = os.getenv("INFLUXDB_DATABASE")

def insert(data=None):
    try:
        status = db.insert(dbname, data)
    except Exception as e:
        respon = {
            "status": False,
            "messages": str(e)
        }
        return respon
    else:
        respon = {
            "status": status,
            "data": data
        }
        return respon

def delete(measurement, tags):
    try:
        status = db.delete(dbname=dbname,
            measurement=measurement,
            tags=tags)
    except Exception as e:
        respon = {
            "status": False,
            "messages": str(e)
        }
        return respon
    else:
        respon = {
            "status": status,
            "measurement": measurement,
            "data": tags,
            "messages": "Deleted"
        }
        return respon

def result(measure_name):
    try:
        dm = db.query(dbname,"SELECT * FROM "+measure_name)
        data_points = list(dm.get_points(measurement=measure_name))
    except Exception as e:
        respon = {
            "messages": str(e)
        }
        return respon
    else:
        respon = {
            "measurement": measure_name,
            "data": data_points
        }
        return respon

def row(measurement, tags):
    try:
        dm = db.query(dbname,"SELECT * FROM "+measurement)
        data_points = list(dm.get_points(measurement=measurement, tags=tags))
    except Exception as e:
        respon = {
            "messages": str(e)
        }
        return respon
    else:
        respon = {
            "measurement": measurement,
            "data": data_points
        }
        return respon

