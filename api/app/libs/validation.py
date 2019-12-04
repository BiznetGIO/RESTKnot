import re
from ipaddress import ip_address
from app.models import model


def is_valid_a(a):
    try:
        ip_address(a)
    except ValueError:
        return True
    else:
        return False


def is_valid_mx(mx):
    if mx == "@":
        return False
    else:
        pattern = re.compile(
            "^(([a-zA-Z0-9_]|[a-zA-Z0-9_][a-zA-Z0-9_\-]*[a-zA-Z0-9_])\.)*([A-Za-z0-9_]|[A-Za-z0-9_\*][A-Za-z0-9_\-]*[A-Za-z0-9_](\.?))$"
        )
        if pattern.match(mx):
            return False
        else:
            return True


def is_valid_cname(cname):
    if cname == "@":
        return False
    else:
        pattern = re.compile(
            "^(([a-zA-Z0-9_]|[a-zA-Z_][a-zA-Z0-9_\-]*[a-zA-Z0-9_])\.)*([A-Za-z0-9_]|[A-Za-z_\*][A-Za-z0-9_\-]*[A-Za-z0-9_](\.?))$"
        )
        if pattern.match(cname):
            return False
        else:
            return True


def is_valid_txt(txt):
    if txt == "@" or txt == "*":
        return False
    else:
        pattern = re.compile("^[\x20-\x7F]*$")
        if pattern.match(txt):
            return False
        else:
            return True


def is_valid_zone(zone):
    pattern = re.compile(
        "^(?!(https:\/\/|http:\/\/|www\.|mailto:|smtp:|ftp:\/\/|ftps:\/\/))(((([a-zA-Z0-9])|([a-zA-Z0-9][a-zA-Z0-9\-]{0,86}[a-zA-Z0-9]))\.(([a-zA-Z0-9])|([a-zA-Z0-9][a-zA-Z0-9\-]{0,73}[a-zA-Z0-9]))\.(([a-zA-Z0-9]{2,12}\.[a-zA-Z0-9]{2,12})|([a-zA-Z0-9]{2,25})))|((([a-zA-Z0-9])|([a-zA-Z0-9][a-zA-Z0-9\-]{0,162}[a-zA-Z0-9]))\.(([a-zA-Z0-9]{2,12}\.[a-zA-Z0-9]{2,12})|([a-zA-Z0-9]{2,25}))))$"
    )
    if pattern.match(zone):
        return False
    else:
        return True


def is_valid_rtype(rtype):
    if rtype == "@" or rtype == "*":
        return False
    else:
        pattern = re.compile(
            "^(([\*a-zA-Z0-9_]|[a-zA-Z0-9_][a-zA-Z0-9\-]*[a-zA-Z0-9])\.)*([A-Za-z0-9]|[_A-Za-z0-9][A-Za-z0-9\-]*[A-Za-z0-9])$"
        )
        if pattern.match(rtype):
            return False
        else:
            return True


def count_character(name):
    if name.find("."):
        spl_name = name.split(".")
        total = 0
        for i in spl_name:
            if len(i) >= 64:
                return True
            else:
                total = total + len(i)
        if total >= 255:
            return True
        else:
            return False
    else:
        return False


def is_valid_rdata(rtype, rdata):
    is_valid = False

    if rtype == "A":
        is_valid = is_valid_a(rdata)
    elif rtype == "MX":
        is_valid = is_valid_mx(rdata)
    elif rtype == "CNAME":
        is_valid = is_valid_cname(rdata)
    elif rtype == "TXT":
        is_valid = is_valid_txt(rdata)
    else:
        return False

    return is_valid
