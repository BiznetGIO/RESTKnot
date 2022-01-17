#  --------------------------------------------------------------------
# DNS Rules
#
# The rules for DNS records:
#
# CNAME
# 1. same owner NOT allowed
# 2. owner CAN'T coexist with the same A owner
#
# A
# 1. same owner allowed
# 2. owner CAN'T coexist with the same CNAME owner
# --------------------------------------------------------------------

from typing import Any, Callable, Dict

from app.models import rtype as rtype_db
from app.models import rules as rules_model
from app.models import zone as zone_db


def is_allowed(
    zone_id: int, rtype_id: int, owner: str, rdata: str, ttl_id: int, _: Any = None
):
    """A Generic function to check is given record is allowed.

    :param Any _: To make it compatible with other similar function. The caller always pass the same amount of args.

    1. Check for duplicate record

    """
    #  duplicate record NOT allowed
    rules = rules_model.Rules()
    rules.is_duplicate(zone_id, rtype_id, owner, rdata, ttl_id)


def is_allowed_cname(zone_id: int, rtype_id: int, owner: str, rdata: str, ttl_id: int):
    """Check is given CNAME record is allowed.

    1. Check for duplicate record
    2. Check for the same owner
    3. Check for the same A owner
    4. Check if the owner is root
    """
    #  duplicate record NOT allowed
    is_allowed(zone_id, rtype_id, owner, rdata, ttl_id)

    # 1. same owner NOT allowed
    rules = rules_model.Rules()
    query = f""" SELECT * FROM "record" WHERE "zone_id" = {zone_id}
            AND "owner" = '{owner}' AND  "rtype_id" = {rtype_id} """
    is_unique = rules.is_unique(query)
    if not is_unique:
        raise ValueError("a CNAME record already exist with that owner")

    # 2. owner CAN'T coexist with the same A owner
    a_type = rtype_db.get_by_value("A")
    if not a_type:
        raise ValueError("type not found")

    a_rtype_id = a_type["id"]
    query = f""" SELECT * FROM "record" WHERE "zone_id" = {zone_id}
            AND "owner" = '{owner}' AND  "rtype_id" IN ({rtype_id},{a_rtype_id}) """

    is_coexist = rules.is_coexist(query)
    if is_coexist:
        raise ValueError("an A record already exist with that owner")

    # 4. owner can't be root
    # can't be `domainname.com.` and `@`
    zone = zone_db.get(zone_id)
    if not zone:
        raise ValueError("zone not found")

    if owner in (f"{zone['zone']}", "@"):
        raise ValueError("a CNAME owner can't be root")


def is_allowed_a(
    zone_id: int, rtype_id: int, owner: str, rdata: str, ttl_id: int, _: Any = None
):
    """Check is given A record is allowed.

    :param Any _: To make it compatible with other similar function. The caller always pass the same amount of args.

    1. Check for duplicate record
    2. Check for the same CNAME owner
    """
    #  duplicate record NOT allowed
    is_allowed(zone_id, rtype_id, owner, rdata, ttl_id)

    # 2. owner CAN'T coexist with the same CNAME owner
    cname_type = rtype_db.get_by_value("CNAME")
    if not cname_type:
        raise ValueError("cname not found")

    cname_rtype_id = cname_type["id"]
    query = f""" SELECT * FROM "record" WHERE "zone_id" = {zone_id}
            AND "owner" = '{owner}' AND  "rtype_id" = {cname_rtype_id} """

    rules = rules_model.Rules()
    is_coexist = rules.is_coexist(query)
    if is_coexist:
        raise ValueError("a CNAME record already exist with that owner")


def is_allowed_cname_edit(
    zone_id: int,
    rtype_id: int,
    owner: str,
    rdata: str,
    ttl_id: int,
    record_id: int = None,
):
    """Check is given CNAME record is allowed.

    This function separated from `cname_add` because it needs to exclude its id
    while searching for other records.
    """
    rules = rules_model.Rules()

    #  duplicate record NOT allowed
    is_allowed(zone_id, rtype_id, owner, rdata, ttl_id)

    # 1. same owner NOT allowed
    query = f""" SELECT * FROM "record" WHERE "zone_id" = {zone_id}
            AND "owner" = '{owner}' AND  "rtype_id" = {rtype_id} AND "id" <> {record_id} """
    is_unique = rules.is_unique(query)
    if not is_unique:
        raise ValueError("a CNAME record already exist with that owner")

    # 2. owner CAN'T coexist with the same A owner
    a_type = rtype_db.get_by_value("A")
    if not a_type:
        raise ValueError("type not found")

    a_rtype_id = a_type["id"]
    query = f""" SELECT * FROM "record" WHERE "zone_id" = {zone_id}
            AND "owner" = '{owner}' AND  "rtype_id" IN ({rtype_id}, {a_rtype_id}) AND "id" <> {record_id} """
    is_coexist = rules.is_coexist(query)
    if is_coexist:
        raise ValueError("an A record already exist with that owner")

    # 3. owner can't be `domainname.com.` and `@`
    zone = zone_db.get(zone_id)
    if not zone:
        raise ValueError("zone not found")

    if owner in (f"{zone['zone']}", "@"):
        raise ValueError("a CNAME owner can't be root")


# function based on rtype input when adding record
functions_add: Dict[str, Callable] = {
    "CNAME": is_allowed_cname,
    "A": is_allowed_a,
    "AAAA": is_allowed_a,
    "SOA": is_allowed,
    "NS": is_allowed,
    "MX": is_allowed,
    "TXT": is_allowed,
}

functions_edit: Dict[str, Callable] = {
    "CNAME": is_allowed_cname_edit,
    "A": is_allowed_a,
    "AAAA": is_allowed_a,
    "SOA": is_allowed,
    "NS": is_allowed,
    "MX": is_allowed,
    "TXT": is_allowed,
}


def check_add(
    rtype: str, zone_id: int, rtype_id: int, owner: str, rdata: str, ttl_id: int
):
    rtype = rtype.upper()
    if rtype in functions_add:
        functions_add[rtype](zone_id, rtype_id, owner, rdata, ttl_id)
    else:
        raise ValueError("unsupported record type")


def check_edit(
    rtype: str,
    zone_id: int,
    rtype_id: int,
    owner: str,
    rdata: str,
    ttl_id: int,
    record_id: int = None,
):
    """Return function when user editing A record.

    Some function need dummy `record_id` parameters to match with other function
    parameter length
    """
    rtype = rtype.upper()
    if rtype in functions_edit:
        functions_edit[rtype](zone_id, rtype_id, owner, rdata, ttl_id, record_id)
    else:
        raise ValueError("unsupported record type")
