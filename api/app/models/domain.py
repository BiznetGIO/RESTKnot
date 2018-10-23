from app import influx
from . import app_models as db
import os, hashlib, time


dbname = os.getenv("INFLUXDB_DATABASE")
measure_name = "domain"
tag_key = hashlib.md5(str(db.timeset()).encode('utf-8')).hexdigest()

def insert(data=None):
    data_prepare = [{
        "measurement": measure_name,
        "tags": {
            "domain_id": measure_name+"_"+tag_key
        },
        "time": db.timeset(),
        "fields": data
    }]
    try:
        status = db.insert(dbname, data_prepare)
    except Exception as e:
        respon = {
            "status": False,
            "messages": str(e)
        }
        return respon
    else:
        respon = {
            "status": status,
            "measurement": measure_name,
            "data": data
        }
        return respon