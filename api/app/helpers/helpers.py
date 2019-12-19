import datetime


def soa_time_set():
    date = datetime.datetime.now().strftime("%Y%m%d")
    return date


def get_datetime():
    now = datetime.datetime.now(datetime.timezone.utc)
    return f"{now:%Y-%m-%d %H:%M:%S %z}"


def exclude_keys(dict_, keys):
    """Exclude specified key from dict."""
    return {item: dict_[item] for item in dict_ if item not in keys}
