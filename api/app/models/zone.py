from typing import Dict, List, Optional

from app.models import model


def get_zone(zone_id: int) -> str:
    """Get zone name by ID"""
    zone = model.get_one(table="zone", field="id", value=f"{zone_id}")
    if not zone:
        raise ValueError("Zone Not Found")

    zone_name = zone["zone"]
    return zone_name


def get_zone_id(zone) -> int:
    zone = model.get_one(table="zone", field="zone", value=f"{zone}")
    if not zone:
        raise ValueError("Zone Not Found")

    zone_id = zone["id"]
    return zone_id


def get_zone_by_record(record_id: int) -> Optional[dict]:
    record = model.get_one(table="record", field="id", value=f"{record_id}")
    if not record:
        raise ValueError("Record Not Found")

    zone_id = record["zone_id"]
    zone = model.get_one(table="zone", field="id", value=f"{zone_id}")
    return zone


def get_zones_by_user(user_id: int) -> List[Dict]:
    query = 'SELECT * FROM "zone" WHERE "user_id"=%(user_id)s'
    value = {"user_id": user_id}
    zones = model.plain_get("zone", query, value)
    return zones
