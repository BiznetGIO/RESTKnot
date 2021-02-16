from app.models import model


def get_zone(zone_id):
    """Get zone name by ID"""
    zone = model.get_one(table="zone", field="id", value=f"{zone_id}")
    if not zone:
        raise ValueError(f"Zone Not Found")

    zone = zone["zone"]
    return zone


def get_zone_id(zone):
    zone = model.get_one(table="zone", field="zone", value=f"{zone}")
    if not zone:
        raise ValueError(f"Zone Not Found")

    zone_id = zone["id"]
    return zone_id


def get_zone_by_record(record_id):
    record = model.get_one(table="record", field="id", value=f"{record_id}")
    zone_id = record["zone_id"]
    zone = model.get_one(table="zone", field="id", value=f"{zone_id}")
    return zone


def get_zones_by_user(user_id):
    query = 'SELECT * FROM "zone" WHERE "user_id"=%(user_id)s'
    value = {"user_id": user_id}
    zones = model.plain_get("zone", query, value)
    return zones
