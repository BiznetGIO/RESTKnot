from app.helpers import helpers

knot_conf_set = {
    "cmd": "conf-set",
    "section": "zone",
    "item": "domain",
    "data": "company.com",
}


# Serial date is dynamic, thus can't be hardcoded
current_time = helpers.soa_time_set()
serial = f"{str(current_time)}01"
rdata = f"one.dns.id. hostmaster.dns.id. {serial} 3600 1800 604800 86400"

knot_zone_set_soa = {
    "cmd": "zone-set",
    "zone": "company.com",
    "owner": "@",
    "rtype": "SOA",
    "ttl": "3600",
    "data": rdata,
}

knot_zone_set_ns = {
    "cmd": "zone-set",
    "zone": "company.com",
    "owner": "@",
    "rtype": "NS",
    "ttl": "3600",
    "data": "one.dns.id.",
}
