import re
from ipaddress import ip_address

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
        # we need to improve this validation.
        # this is a loose validation
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
    """Check if it's a valid domain name."""
    match = re.match(RE_ZONE, domain_name)
    if match is None:
        raise ValueError("Bad Domain Name")


def is_valid_soa(soa_rdata):
    """Simple function to check SOA RDATA."""
    rdatas = soa_rdata.split(" ")

    try:
        is_valid_cname(rdatas[0])
        is_valid_cname(rdatas[1])
    except Exception:
        raise ValueError("Bad SOA RDATA")

    for number in rdatas[2:]:
        try:
            int(number)
        except ValueError:
            raise ValueError("Bad SOA RDATA")


functions = {
    "A": is_valid_ip,
    "AAAA": is_valid_ip,
    "MX": is_valid_mx,
    "CNAME": is_valid_cname,
    "NS": is_valid_cname,
    "EMAIL": is_valid_email,
    "ZONE": is_valid_zone,
    "SOA": is_valid_soa,
}


def validate(rtype, rdata):
    if rtype in functions.keys():
        functions[rtype](rdata)
