from app.models import model


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
