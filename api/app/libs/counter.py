from app.models import model
from app import db


def update_counter(nm_zone):
    filter_zone = model.get_by_id("zn_zone", "nm_zone", nm_zone)[0]
    id_zone = filter_zone['id_zone']
    counter = filter_zone['counter']
    update_count = {
        'where': {
            "id_zone": str(id_zone)
        },
        'data': {
            "counter" : str(counter+1)
        }
    }
    a = model.update("zn_zone", update_count)
    