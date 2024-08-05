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

from rkapi.app.models import rules as rules_model
from rkapi.app.models import type_ as type_model
from rkapi.app.models import zone as zone_model


def is_allowed(zone_id, type_id, owner, rdata, ttl_id, record_id=None):
    """A Generic function to check is given record is allowed.

    1. Check for duplicate record
    """
    #  duplicate record NOT allowed
    rules = rules_model.Rules()
    rules.is_duplicate(zone_id, type_id, owner, rdata, ttl_id)


def is_allowed_cname(zone_id, type_id, owner, rdata, ttl_id):
    """Check is given CNAME record is allowed.

    1. Check for duplicate record
    2. Check for the same owner
    3. Check for the same A owner
    4. Check if the owner is root
    """
    #  duplicate record NOT allowed
    is_allowed(zone_id, type_id, owner, rdata, ttl_id)

    # 1. same owner NOT allowed
    query = '"type_id"=%(type_id)s AND "owner"=%(owner)s'
    value = {"zone_id": zone_id, "type_id": type_id, "owner": owner}
    rules = rules_model.Rules(query, value)

    is_unique = rules.is_unique()
    if not is_unique:
        raise ValueError("A CNAME record already exist with that owner")

    # 2. owner CAN'T coexist with the same A owner
    a_type_id = type_model.get_typeid_by_rtype("A")
    query = '"type_id" IN (%(type1)s,%(type2)s) AND "owner"=%(owner)s'
    value = {"zone_id": zone_id, "type1": type_id, "type2": a_type_id, "owner": owner}
    rules = rules_model.Rules(query, value)

    is_coexist = rules.is_coexist()
    if is_coexist:
        raise ValueError("An A record already exist with that owner")

    # 4. owner can't be root
    # can't be `domainname.com.` and `@`
    zone = zone_model.get_zone(zone_id)
    if owner == f"{zone}." or owner == "@":
        raise ValueError("A CNAME owner can't be root")


def is_allowed_a(zone_id, type_id, owner, rdata, ttl_id, record_id=None):
    """Check is given A record is allowed.

    1. Check for duplicate record
    2. Check for the same CNAME owner
    """
    #  duplicate record NOT allowed
    is_allowed(zone_id, type_id, owner, rdata, ttl_id)

    # 2. owner CAN'T coexist with the same CNAME owner
    cname_type_id = type_model.get_typeid_by_rtype("CNAME")
    query = '"type_id"=%(type_id)s AND "owner"=%(owner)s'
    value = {"zone_id": zone_id, "type_id": cname_type_id, "owner": owner}
    rules = rules_model.Rules(query, value)

    is_coexist = rules.is_coexist()
    if is_coexist:
        raise ValueError("A CNAME record already exist with that owner")


def is_allowed_cname_edit(zone_id, type_id, owner, rdata, ttl_id, record_id=None):
    """Check is given CNAME record is allowed.

    This function separated from `cname_add` because it needs to exclude its id
    while searching for other records.
    """
    #  duplicate record NOT allowed
    is_allowed(zone_id, type_id, owner, rdata, ttl_id)

    # 1. same owner NOT allowed
    query = '"type_id"=%(type_id)s AND "owner"=%(owner)s AND "id"<>%(record_id)s'
    value = {
        "zone_id": zone_id,
        "type_id": type_id,
        "owner": owner,
        "record_id": record_id,
    }
    rules = rules_model.Rules(query, value)

    is_unique = rules.is_unique()
    if not is_unique:
        raise ValueError("A CNAME record already exist with that owner")

    # 2. owner CAN'T coexist with the same A owner
    a_type_id = type_model.get_typeid_by_rtype("A")
    query = '"type_id" IN (%(type1)s,%(type2)s) AND "owner"=%(owner)s AND "id"<>%(record_id)s'
    value = {
        "zone_id": zone_id,
        "type1": type_id,
        "type2": a_type_id,
        "owner": owner,
        "record_id": record_id,
    }
    rules = rules_model.Rules(query, value)

    is_coexist = rules.is_coexist()
    if is_coexist:
        raise ValueError("An A record already exist with that owner")

    # 3. owner can't be root
    zone = zone_model.get_zone(zone_id)
    if owner == f"{zone}." or owner == "@":
        raise ValueError("A CNAME owner can't be root")


# function based on rtype input when adding record
functions_add = {
    "CNAME": is_allowed_cname,
    "A": is_allowed_a,
    "AAAA": is_allowed_a,
    "SOA": is_allowed,
    "NS": is_allowed,
    "MX": is_allowed,
    "TXT": is_allowed,
    "SRV": is_allowed,
}
functions_edit = {
    "CNAME": is_allowed_cname_edit,
    "A": is_allowed_a,
    "AAAA": is_allowed_a,
    "SOA": is_allowed,
    "NS": is_allowed,
    "MX": is_allowed,
    "TXT": is_allowed,
    "SRV": is_allowed,
}


def check_add(rtype, zone_id, type_id, owner, rdata, ttl_id):
    rtype = rtype.upper()
    if rtype in functions_add.keys():
        functions_add[rtype](zone_id, type_id, owner, rdata, ttl_id)
    else:
        raise ValueError("Unsupported Record Type")


def check_edit(rtype, zone_id, type_id, owner, rdata, ttl_id, record_id=None):
    """Return function when user editing A record.

    Some function need dummy `record_id` parameters to match with other function
    parameter length
    """
    rtype = rtype.upper()
    if rtype in functions_edit.keys():
        functions_edit[rtype](zone_id, type_id, owner, rdata, ttl_id, record_id)
    else:
        raise ValueError("Unsupported Record Type")
