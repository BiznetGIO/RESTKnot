import requests
import datetime
from app.controllers.api import record as record_api
from app.models import model


def soa_time_set():
    date = datetime.datetime.now().strftime("%Y%m%d")
    return date


def get_http(url, param=None, header=None):
    json_data = None
    if param:
        json_data = param
    get_func = requests.get(url, params=json_data, headers=header)
    data = get_func.json()
    return data


def get_datetime():
    now = datetime.datetime.now()
    return str(now)


def check_unique(stored, field, value, key=None):
    results = False
    try:
        all_data = model.get_all(stored)
    except Exception:
        results = False
    else:
        for i in all_data:
            if i[field] == value:
                if key is not None:
                    if key == i["key"]:
                        results = False
                    else:
                        results = True
                else:
                    results = True
                break
    return results


def get_last_key(stored):
    try:
        all_data = model.read_all_key(stored)
    except Exception:
        return str(1)
    else:
        key = max(all_data)
        return str(key + 1)


def check_record_serial(id_):
    try:
        record = model.get_by_id(table="record", field="id", id_=id_)
    except Exception as e:
        raise e
    else:
        # hardcode 0 because record will
        # always contains one result
        return record[0]["is_serial"]
