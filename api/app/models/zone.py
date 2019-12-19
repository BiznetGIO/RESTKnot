from app.models import model


def get_zone_id(zone):
    zone = model.get_one(table="zone", field="zone", value=f"{zone}")
    if not zone:
        raise ValueError(f"Zone Not Found")

    zone_id = zone["id"]
    return zone_id
