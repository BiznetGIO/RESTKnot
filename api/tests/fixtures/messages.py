knot_conf_set = {
    "cmd": "conf-set",
    "section": "zone",
    "item": "domain",
    "data": "company.com",
}
knot_zone_set_ns = {
    "cmd": "zone-set",
    "zone": None,
    "owner": "@",
    "rtype": "NS",
    "ttl": "3600",
    "data": "satu.neodns.id.",
}

knot_delegate_file = {
    "item": "file",
    "data": "company.com.zone",
    "identifier": "company.com",
    "cmd": "conf-set",
    "section": "zone",
    "zone": "company.com",
}
