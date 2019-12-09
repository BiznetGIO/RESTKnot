from app.models import model


def get_zone_id(zone):
    try:
        zone = model.get_one(table="zone", field="zone", value=f"{zone}")
        zone_id = zone["id"]
        return zone_id
    except IndexError:
        raise ValueError(f"Zone Not Found")
