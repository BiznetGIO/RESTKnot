#  --------------------------------------------------------------------
# RDATA Rules
#
# The rules for DNS RDATA:
#
# IP
# EMAIL
# MX
# CNAME
# ZONE
# SOA
#
#
#
# Credits:
# RE Email Credit: https://emailregex.com/
# RE ZONE Credit:
# RE CNAME Credit: https://www.regextester.com/106386
# --------------------------------------------------------------------

from typing import Callable, Dict

import re
import string
from ipaddress import ip_address

RE_EMAIL = "(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
RE_ZONE = "^(?!(https:\/\/|http:\/\/|www\.|mailto:|smtp:|ftp:\/\/|ftps:\/\/))(((([a-zA-Z0-9])|([a-zA-Z0-9][a-zA-Z0-9\-]{0,86}[a-zA-Z0-9]))\.(([a-zA-Z0-9])|([a-zA-Z0-9][a-zA-Z0-9\-]{0,73}[a-zA-Z0-9]))\.(([a-zA-Z0-9]{2,12}\.[a-zA-Z0-9]{2,12})|([a-zA-Z0-9]{2,25})))|((([a-zA-Z0-9])|([a-zA-Z0-9][a-zA-Z0-9\-]{0,162}[a-zA-Z0-9]))\.(([a-zA-Z0-9]{2,12}\.[a-zA-Z0-9]{2,12})|([a-zA-Z0-9]{2,25}))))$"
RE_CNAME = "^(([a-zA-Z0-9_]|[a-zA-Z0-9_][a-zA-Z0-9_\-]*[a-zA-Z0-9_])\.)*([A-Za-z0-9_]|[A-Za-z0-9_][A-Za-z0-9_\-]*[A-Za-z0-9_](\.?))$"


def is_valid_ip(ip: str):
    """Check whether it's a valid IPv4 or IPv6."""
    try:
        ip_address(ip)
    except ValueError:
        raise ValueError("bad IP address")


def is_valid_email(email: str):
    """Check if  it's a valid email address."""
    match = re.match(RE_EMAIL, email)
    if match is None:
        raise ValueError("bad email address")


def is_valid_mx(mx_rdata: str):
    """Check if  MX RDATA contents is valid."""
    msg = "bad MX rdata"

    preference = mx_rdata.split(" ")[0]
    hostname = mx_rdata.split(" ")[1]

    try:
        # we need to improve this validation.
        # this is a loose validation
        if (int(preference)).bit_length() <= 16 and len(mx_rdata.split(" ")) == 2:
            pass
        else:
            raise ValueError(msg)
    except Exception:
        raise ValueError(msg)

    try:
        is_valid_cname(hostname)
    except Exception:
        raise ValueError(msg)


def is_valid_cname(cname_rdata: str):
    """Check if  CNAME RDATA contents is valid."""
    msg = "bad CNAME rdata"

    if cname_rdata == "@":
        raise ValueError(msg)

    match = re.match(RE_CNAME, cname_rdata)
    if match is None:
        raise ValueError(msg)


def is_valid_zone(domain_name: str):
    """Check if it's a valid domain name."""
    match = re.match(RE_ZONE, domain_name)
    if match is None:
        raise ValueError("bad domain name")


def is_valid_txt(txt_rdata: str):
    """Check if it's a valid TXT rdata."""
    for char in txt_rdata:
        if char not in string.printable:
            raise ValueError("bad TXT rdata")


def is_valid_soa(soa_rdata: str):
    """Simple function to check SOA RDATA."""
    rdatas = soa_rdata.split(" ")

    try:
        is_valid_cname(rdatas[0])
        is_valid_cname(rdatas[1])
    except Exception:
        raise ValueError("bad SOA rdata")

    for number in rdatas[2:]:
        try:
            int(number)
        except ValueError:
            raise ValueError("bad SOA rdata")


def is_valid_owner(owner: str):
    """Check if it's a valid owner.

    Rules:
    - owner label can't end with dot (".")
    - owner label can't ends/starts with dash ("-")
    - owner can't exceed 255 characters
    - owner label can't exceed 63 characters
    - owner can't contains parens ("()")
    """

    def check_hypen(label):
        if any((label.endswith("."), label.endswith("-"), label.startswith("-"))):
            raise ValueError("bad owner")

    check_hypen(owner)

    if "." in owner:
        for label in owner.split("."):
            check_hypen(label)

    if len(owner) > 255:
        raise ValueError("bad owner")

    if "." in owner:
        for label in owner.split("."):
            if len(label) > 63:
                raise ValueError("bad owner")

    if any(char in "()" for char in owner):
        raise ValueError("bad owner")


functions: Dict[str, Callable] = {
    "A": is_valid_ip,
    "AAAA": is_valid_ip,
    "MX": is_valid_mx,
    "CNAME": is_valid_cname,
    "NS": is_valid_cname,
    "EMAIL": is_valid_email,
    "ZONE": is_valid_zone,
    "SOA": is_valid_soa,
    "TXT": is_valid_txt,
    "OWNER": is_valid_owner,
}


def validate(rtype: str, rdata: str):
    if not rdata:
        raise ValueError("rdata can't be empty")

    rtype = rtype.upper()
    if rtype in functions:
        functions[rtype](rdata)
    else:
        raise ValueError("unsupported record type")
