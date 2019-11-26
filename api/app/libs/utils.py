import datetime
from app.models import model


def soa_time_set():
    date = datetime.datetime.now().strftime("%Y%m%d")
    return date


def get_datetime():
    # FIXME use global UTC time. not local
    now = datetime.datetime.now()
    return str(now)


def check_record_serial(id_):
    try:
        record = model.get_by_id(table="record", field="id", id_=id_)
    except Exception as e:
        raise e
    else:
        # hardcode 0 because record will
        # always contains one result
        return record[0]["is_serial"]
