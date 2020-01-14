from app.models import model
from app.helpers import helpers
from app.models import zone as zone_model
from app.models import type_ as type_model


def get_other_data(record):
    rdata = model.get_one(table="rdata", field="record_id", value=record["id"])
    zone = model.get_one(table="zone", field="id", value=record["zone_id"])
    ttl = model.get_one(table="ttl", field="id", value=record["ttl_id"])
    type_ = model.get_one(table="type", field="id", value=record["type_id"])

    rdata = helpers.exclude_keys(rdata, {"id", "record_id"})
    zone = helpers.exclude_keys(zone, {"id", "is_committed", "user_id", "record_id"})

    data = {
        "id": record["id"],
        "owner": record["owner"],
        "rdata": rdata,
        "zone": zone,
        "type": type_,
        "ttl": ttl,
    }

    return data


def is_exists(record_id):
    record = model.get_one(table="record", field="id", value=record_id)
    if not record:
        raise ValueError(f"Record Not Found")


def is_duplicate_owner(zone_id, type_id, owner):
    query = 'SELECT * FROM "record" WHERE "zone_id"=%(zone_id)s AND "type_id"=%(type_id)s AND "owner"=%(owner)s'
    value = {"zone_id": zone_id, "type_id": type_id, "owner": owner}
    records = model.plain_get("record", query, value)

    if records:  # initial database will return None
        if len(records) != 0:
            raise ValueError(f"Can't Have Multiple Record with Same Owner")


def get_records_by_zone(zone):
    zone_id = zone_model.get_zone_id(zone)

    query = 'SELECT * FROM "record" WHERE "zone_id"=%(zone_id)s'
    value = {"zone_id": zone_id}
    records = model.plain_get("record", query, value)
    return records


def get_soa_record(zone):
    records = get_records_by_zone(zone)

    for record in records:
        rtype = type_model.get_type_by_recordid(record["id"])
        if rtype == "SOA":
            return record
