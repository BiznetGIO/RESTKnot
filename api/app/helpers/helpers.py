import datetime
from functools import wraps
from app.helpers import producer
from app.vendors.rest import response


def soa_time_set():
    date = datetime.datetime.now().strftime("%Y%m%d")
    return date


def replace_serial(rdata, serial):
    """Replace serial value in  given rdata."""
    rdatas = rdata.split(" ")
    # `mname_and_rname` contains such 'one.dns.id. two.dns.id.'
    # `ttls` contains such '10800 3600 604800 38400'
    mname_and_rname = " ".join(rdatas[0:2])
    ttls = " ".join(rdatas[3:])

    return f"{mname_and_rname} {serial} {ttls}"


def increment_serial(serial, increment="01"):
    """Increment serial value with given str value.

    Keyword arguments:
    increment -- the increment value (default "01")
    """
    # The 10-digit serial (YYYYMMDDnn) is incremented, the first
    # 8 digits match the current iso-date
    nn = serial[-2:]
    if int(nn) > 97:  # knot maximum of nn is 99
        # 97 was chosen because serial
        #  increment can be twice at time
        raise ValueError("Zone Change Limit Reached")
    increment = add_str(nn, increment)
    current_time = soa_time_set()
    return f"{current_time}{increment}"


def get_datetime():
    now = datetime.datetime.now(datetime.timezone.utc)
    return f"{now:%Y-%m-%d %H:%M:%S %z}"


def exclude_keys(dict_, keys):
    """Exclude specified key from dict."""
    return {item: dict_[item] for item in dict_ if item not in keys}


def add_str(x, y):
    """Handle string addition

    :Example:
    add_str('11', '01') => '12'
    """
    return str(int(x) + int(y)).zfill(len(x))


def check_producer(f):
    """Check producer availability"""

    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            producer.kafka_producer()
        except Exception as e:
            return response(500, message=f"{e}")
        else:
            return f(*args, **kwargs)

    return decorated_function
