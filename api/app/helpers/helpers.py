import datetime


def soa_time_set():
    date = datetime.datetime.now().strftime("%Y%m%d")
    return date


def replace_serial(rdata, serial):
    rdatas = rdata.split(" ")
    # `mname_and_rname` contains such 'one.dns.id. two.dns.id.'
    # `ttls` contains such '10800 3600 604800 38400'
    mname_and_rname = " ".join(rdatas[0:2])
    ttls = " ".join(rdatas[3:])

    return f"{mname_and_rname} {serial} {ttls}"


def increment_serial(serial):
    # The 10-digit serial (YYYYMMDDnn) is incremented, the first
    # 8 digits match the current iso-date
    nn = serial[-2:]
    increment = add_str(nn, "01")
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
