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

from app.models import rules as rules_model
from app.models import type_ as type_model


def is_allowed_cname(zone_id, type_id, owner):
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


def is_allowed_a(zone_id, type_id, owner):
    # 2. owner CAN'T coexist with the same CNAME owner
    cname_type_id = type_model.get_typeid_by_rtype("CNAME")
    query = '"type_id"=%(type_id)s AND "owner"=%(owner)s'
    value = {"zone_id": zone_id, "type_id": cname_type_id, "owner": owner}
    rules = rules_model.Rules(query, value)

    is_coexist = rules.is_coexist()
    if is_coexist:
        raise ValueError("A CNAME record already exist with that owner")


# function based on rtype input when adding record
functions = {"CNAME": is_allowed_cname, "A": is_allowed_a}


def check(rtype, zone_id, type_id, owner):
    rtype = rtype.upper()
    if rtype in functions.keys():
        functions[rtype](zone_id, type_id, owner)
