import datetime


def soa_time_set():
    date = datetime.datetime.now().strftime("%Y%m%d")
    return date


def get_datetime():
    # FIXME use global UTC time. not local
    now = datetime.datetime.now()
    return str(now)


def exclude_keys(dict_, keys):
    """Exclude specified key from dict."""
    return {item: dict_[item] for item in dict_ if item not in keys}
