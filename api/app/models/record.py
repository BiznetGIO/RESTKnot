from typing import Dict, Optional

from flask import current_app

from app.helpers import helpers
from app.models import model
from app.models import type_ as type_model
from app.models import zone as zone_model


def get_other_data(record: Dict) -> Optional[Dict]:
    try:
        rdata = model.get_one(table="rdata", field="record_id", value=record["id"])
        zone = model.get_one(table="zone", field="id", value=record["zone_id"])
        ttl = model.get_one(table="ttl", field="id", value=record["ttl_id"])
        type_ = model.get_one(table="type", field="id", value=record["type_id"])

        if rdata:
            rdata = helpers.exclude_keys(rdata, {"id", "record_id"})
            rdata = rdata.get("rdata")

        zone = helpers.exclude_keys(
            zone, {"id", "is_committed", "user_id", "record_id"}
        )

        data = {
            "id": record["id"],
            "owner": record["owner"],
            "rdata": rdata,
            "zone": zone["zone"],
            "type": type_["type"],
            "ttl": ttl["ttl"],
        }

        return data
    except Exception as e:
        current_app.logger.error(f"{e}")
        return None  # for typing purpose


def is_exists(record_id: int):
    record = model.get_one(table="record", field="id", value=record_id)
    if not record:
        raise ValueError("Record Not Found")


def get_records_by_zone(zone) -> Dict:
    zone_id = zone_model.get_zone_id(zone)

    query = 'SELECT * FROM "record" WHERE "zone_id"=%(zone_id)s'
    value = {"zone_id": zone_id}
    records = model.plain_get("record", query, value)
    return records


def get_soa_record(zone) -> Optional[Dict]:
    records = get_records_by_zone(zone)

    for record in records:
        rtype = type_model.get_type_by_recordid(record["id"])
        if rtype == "SOA":
            return record

    return None
