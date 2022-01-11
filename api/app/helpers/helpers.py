import datetime
import os
import pathlib

import yaml


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
    today_date = soa_time_set()
    record_date = serial[:-2]
    # The 10-digit serial (YYYYMMDDnn) is incremented, the first
    # 8 digits match the current iso-date
    nn = serial[-2:]
    if record_date != today_date:
        # date changed, reset `nn`
        nn = "01"

    increment = add_str(nn, increment)
    return f"{today_date}{increment}"


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


def read_file(other_file_name, filename):
    root_dir = pathlib.Path(other_file_name).resolve().parent
    path = root_dir.joinpath(filename)

    if path.is_file():
        with open(path, "rb") as f:
            content = f.read().decode("utf-8")
            return content


def read_version(other_file_name, filename):
    """Read the the current version or build of the app"""
    version = ""

    version = read_file(other_file_name, filename)
    if version:
        version = version.rstrip()

    if not version:
        version = "__UNKNOWN__"

    return version


def config_file():
    """Return config file path."""
    path = os.environ.get("RESTKNOT_CONFIG_FILE")
    if not path:
        current_path = pathlib.Path(__file__)
        path = current_path.parents[2].joinpath("config.yml")

    is_exists = os.path.exists(path)
    if is_exists:
        return path
    else:
        raise ValueError(f"Config File Not Found: {path}")


def get_config():
    """Return config file content."""
    file_ = config_file()
    with open(file_, "r", encoding="utf-8") as opened_file:
        config = yaml.safe_load(opened_file)
        return config
