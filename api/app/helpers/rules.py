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

from app.models import record as record_model
from app.models import type_ as type_model


def is_allowed_cname(zone_id, type_id, owner):
    # 1. same owner NOT allowed
    is_unique = record_model.is_unique(zone_id, type_id, owner)
    if not is_unique:
        raise ValueError("A CNAME record already exist with that owner")

    # 2. owner CAN'T coexist with the same A owner
    a_type_id = type_model.get_typeid_by_rtype("A")
    types = (type_id, a_type_id)
    is_coexist = record_model.is_coexist(zone_id, types, owner)
    if is_coexist:
        raise ValueError("An A record already exist with that owner")


def is_allowed_a(zone_id, type_id, owner):
    # 2. owner CAN'T coexist with the same CNAME owner
    cname_type_id = type_model.get_typeid_by_rtype("CNAME")
    types = (type_id, cname_type_id)
    is_coexist = record_model.is_coexist(zone_id, types, owner)
    if is_coexist:
        raise ValueError("A CNAME record already exist with that owner")


# function based on rtype input when adding record
functions = {"CNAME": is_allowed_cname, "A": is_allowed_a}


def check(rtype, zone_id, type_id, owner):
    rtype = rtype.upper()
    if rtype in functions.keys():
        functions[rtype](zone_id, type_id, owner)
