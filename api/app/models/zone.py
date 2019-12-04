from app.models import model


def get_zone_id(zone):
    try:
        zones = model.get_by_condition(table="zone", field="zone", value=f"{zone}")
        zone_id = zones[0]["id"]
        return zone_id
    except IndexError:
        raise ValueError(f"Zone Not Found")
