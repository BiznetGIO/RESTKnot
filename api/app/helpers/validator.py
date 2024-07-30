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

import re
import string
from ipaddress import ip_address

RE_EMAIL = "(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
RE_ZONE = "^(?!(https:\/\/|http:\/\/|www\.|mailto:|smtp:|ftp:\/\/|ftps:\/\/))(((([a-zA-Z0-9])|([a-zA-Z0-9][a-zA-Z0-9\-]{0,86}[a-zA-Z0-9]))\.(([a-zA-Z0-9])|([a-zA-Z0-9][a-zA-Z0-9\-]{0,73}[a-zA-Z0-9]))\.(([a-zA-Z0-9]{2,12}\.[a-zA-Z0-9]{2,12})|([a-zA-Z0-9]{2,25})))|((([a-zA-Z0-9])|([a-zA-Z0-9][a-zA-Z0-9\-]{0,162}[a-zA-Z0-9]))\.(([a-zA-Z0-9]{2,12}\.[a-zA-Z0-9]{2,12})|([a-zA-Z0-9]{2,25}))))$"
RE_CNAME = "^(([a-zA-Z0-9_]|[a-zA-Z0-9_][a-zA-Z0-9_\-]*[a-zA-Z0-9_])\.)*([A-Za-z0-9_]|[A-Za-z0-9_][A-Za-z0-9_\-]*[A-Za-z0-9_](\.?))$"


def is_valid_ip(ip):
    """Check whether it's a valid IPv4 or IPv6."""
    try:
        ip_address(ip)
    except ValueError:
        raise ValueError("Bad IP Address")


def is_valid_email(email):
    """Check if  it's a valid email address."""
    match = re.match(RE_EMAIL, email)
    if match is None:
        raise ValueError("Bad Email Address")


def is_valid_mx(mx_rdata):
    """Check if  MX RDATA contents is valid."""
    msg = "Bad MX RDATA"

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


def is_valid_txt(txt_rdata):
    """Check if it's a valid TXT rdata."""
    for char in txt_rdata:
        if char not in string.printable:
            raise ValueError("Bad TXT RDATA")


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


def is_valid_srv(rdata):
    """Simple function to check SRV RDATA."""
    rdatas = rdata.split(" ")
    if len(rdatas) != 4:
        raise ValueError("Bad SRV RDATA")

    try:
        is_valid_cname(rdatas[3])
    except Exception:
        raise ValueError("Bad SRV RDATA")

    for number in rdatas[:3]:
        try:
            int(number)
        except ValueError:
            raise ValueError("Bad SRV RDATA")


def is_valid_owner(owner):
    """Check if it's a valid owner.

    Rules:
    - owner label can't end with dot (".")
    - owner label can't ends/starts with dash ("-")
    - owner can't exceed 255 characters
    - owner label can't exceed 63 characters
    - owner can't contains parens ("()")
    """

    def check_hyphen(label):
        if any((label.endswith("."), label.endswith("-"), label.startswith("-"))):
            raise ValueError("Bad OWNER")

    check_hyphen(owner)

    if "." in owner:
        for label in owner.split("."):
            check_hyphen(label)

    if len(owner) > 255:
        raise ValueError("Bad OWNER")

    if "." in owner:
        for label in owner.split("."):
            if len(label) > 63:
                raise ValueError("Bad OWNER")

    if any(char in "()" for char in owner):
        raise ValueError("Bad OWNER")


def is_valid_srv_owner(owner):
    """Check if it's a valid srv owner.

    Rules:
    - must contain service and protocol name
    - can't contain the zone name
    - enfore the service name to be prefixed with _
    - enfore the protocol to be prefixed with _
    """

    if "." not in owner:
        raise ValueError("Bad OWNER")

    labels = owner.split(".")
    if len(labels) < 2:
        raise ValueError("Bad OWNER")

    service_name = labels[0]
    protocol_type = labels[1]
    if not service_name.startswith("_"):
        raise ValueError("Service name must start with underscore")
    if not protocol_type.startswith("_"):
        raise ValueError("Protocol type must start with underscore")

    is_valid_owner(owner)


functions = {
    "A": is_valid_ip,
    "AAAA": is_valid_ip,
    "MX": is_valid_mx,
    "CNAME": is_valid_cname,
    "NS": is_valid_cname,
    "EMAIL": is_valid_email,
    "ZONE": is_valid_zone,
    "SOA": is_valid_soa,
    "TXT": is_valid_txt,
    "SRV": is_valid_srv,
    "OWNER": is_valid_owner,
    "OWNER-SRV": is_valid_srv_owner,
}


def validate(rtype, rdata):
    if not rdata:
        raise ValueError("RDATA can't be empty")

    rtype = rtype.upper()
    if rtype in functions.keys():
        functions[rtype](rdata)
    else:
        raise ValueError("Unsupported Record Type")
