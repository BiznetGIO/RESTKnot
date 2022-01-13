import datetime
import os
import pathlib
from typing import Dict, Optional, Set

import yaml


def soa_time_set() -> str:
    date = datetime.datetime.now().strftime("%Y%m%d")
    return date


def replace_serial(rdata: str, serial: str) -> str:
    """Replace serial value in  given rdata."""
    rdatas = rdata.split(" ")
    # `mname_and_rname` contains such 'one.dns.id. two.dns.id.'
    # `ttls` contains such '10800 3600 604800 38400'
    mname_and_rname = " ".join(rdatas[0:2])
    ttls = " ".join(rdatas[3:])

    return f"{mname_and_rname} {serial} {ttls}"


def increment_serial(serial: str, increment: str = "01") -> str:
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


def get_datetime() -> str:
    now = datetime.datetime.now(datetime.timezone.utc)
    return f"{now:%Y-%m-%d %H:%M:%S %z}"


def exclude_keys(dict_: Dict, keys: Set[str]) -> Dict:
    """Exclude specified key from dict."""
    return {item: dict_[item] for item in dict_ if item not in keys}


def add_str(x: str, y: str) -> str:
    """Handle string addition

    :Example:
    add_str('11', '01') => '12'
    """
    return str(int(x) + int(y)).zfill(len(x))


def read_file(path: pathlib.Path) -> Optional[str]:
    """Read the file content"""
    if path.is_file():
        with open(path, "rb") as f:
            content = f.read().decode("utf-8")
            return content

    return None


def _parse_version(path: pathlib.Path) -> str:
    """Parse the version from a file"""
    version = None

    version = read_file(path)
    if version:
        version = version.rstrip()

    if not version:
        version = "__UNKNOWN__"

    return version


def app_version() -> Dict[str, str]:
    """Return the VCS hash and semantic version of the app"""
    root_dir = pathlib.Path("autoapp.py").resolve().parent
    vcs_revision_file_path = root_dir.joinpath("vcs_revision.txt")

    vcs_revision = _parse_version(vcs_revision_file_path)

    version = {"vcs_revision": vcs_revision}
    return version


def config_file() -> pathlib.Path:
    """Return config file path."""
    custom_path = os.environ.get("RESTKNOT_CONFIG_FILE")
    if not custom_path:
        _current_path = pathlib.Path(__file__)
        default_path = _current_path.parents[2].joinpath("config.yml")

    is_exists = os.path.exists(default_path)
    if is_exists:
        return default_path
    else:
        raise ValueError(f"config file not found: {default_path}")


def get_config() -> Dict:
    """Return config file content."""
    file_ = config_file()
    with open(file_, "r", encoding="utf-8") as opened_file:
        config = yaml.safe_load(opened_file)
        return config
