import re
from ipaddress import ip_address

from app.models import model


"""
RE Email Credit: https://emailregex.com/
RE ZONE Credit:
RE CNAME Credit: https://www.regextester.com/106386
"""

RE_EMAIL = "(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
RE_ZONE = "^(?!(https:\/\/|http:\/\/|www\.|mailto:|smtp:|ftp:\/\/|ftps:\/\/))(((([a-zA-Z0-9])|([a-zA-Z0-9][a-zA-Z0-9\-]{0,86}[a-zA-Z0-9]))\.(([a-zA-Z0-9])|([a-zA-Z0-9][a-zA-Z0-9\-]{0,73}[a-zA-Z0-9]))\.(([a-zA-Z0-9]{2,12}\.[a-zA-Z0-9]{2,12})|([a-zA-Z0-9]{2,25})))|((([a-zA-Z0-9])|([a-zA-Z0-9][a-zA-Z0-9\-]{0,162}[a-zA-Z0-9]))\.(([a-zA-Z0-9]{2,12}\.[a-zA-Z0-9]{2,12})|([a-zA-Z0-9]{2,25}))))$"
RE_CNAME = "^(([a-zA-Z0-9_]|[a-zA-Z0-9_][a-zA-Z0-9_\-]*[a-zA-Z0-9_])\.)*([A-Za-z0-9_]|[A-Za-z0-9_][A-Za-z0-9_\-]*[A-Za-z0-9_](\.?))$"


def is_valid_ip(ip):
    """Check whether it's a valid IPv4 or IPv6."""
    try:
        ip_address(ip)
    except ValueError:
        raise ValueError("Bad IP Adrress")


def is_valid_email(email):
    """Check if  it's a valid email address."""
    match = re.match(RE_EMAIL, email)
    if match is None:
        raise ValueError("Bad Email Adrress")


def is_valid_mx(mx_rdata):
    """Check if  MX RDATA contents is valid."""
    msg = "Bad MX RDATA"

    preference = mx_rdata.split(" ")[0]

    try:
        if (int(preference)).bit_length() <= 16 and len(mx_rdata.split(" ")) == 2:
            pass
        else:
            raise ValueError(msg)
    except Exception:
        raise ValueError(msg)


def is_valid_cname(cname_rdata):
    """Check if  CNAME RDATA contents is valid."""
    msg = "Bad CNAME RDATA"

    if cname_rdata == "@":
        raise ValueError(msg)

    match = re.match(RE_CNAME, cname_rdata)
    if match is None:
        raise ValueError(msg)


def is_valid_zone(domain_name):
    match = re.match(RE_ZONE, domain_name)
    if match is None:
        raise ValueError("Bad Domain Name")


def is_valid_rtype(rtype):
    types = model.get_by_condition(table="type", field="type", value=rtype.upper())
    if types == []:
        raise ValueError("Unrecognized Record Type")


def count_character(name):
    if name.find("."):
        spl_name = name.split(".")
        total = 0
        for i in spl_name:
            if len(i) >= 64:
                pass
            else:
                total = total + len(i)
        if total >= 255:
            pass
        else:
            raise ValueError("Character Length Exceeded")
    else:
        raise ValueError("Character Length Exceeded")


functions = {
    "A": is_valid_ip,
    "MX": is_valid_mx,
    "CNAME": is_valid_cname,
    "EMAIL": is_valid_email,
    "ZONE": is_valid_zone,
    "RTYPE": is_valid_rtype,
    "COUNT": count_character,
}


def validate(rtype, rdata):
    functions[rtype](rdata)
