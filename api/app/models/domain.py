from app.models import model
from app.models import record as record_model
from app.helpers import helpers


def get_other_data(zone):
    if zone is None:
        return

    user = model.get_one(table="user", field="id", value=zone["user_id"])
    user = helpers.exclude_keys(user, {"created_at"})
    records = record_model.get_records_by_zone(zone["zone"])

    records_detail = []
    for record in records:
        record_detail = record_model.get_other_data2(record)
        record_detail = helpers.exclude_keys(record_detail, {"zone"})
        records_detail.append(record_detail)

    data = {
        "zone_id": zone["id"],
        "zone": zone["zone"],
        "user": user,
        "records": records_detail,
    }

    return data
