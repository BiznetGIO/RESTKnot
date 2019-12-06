from app.models import model


def get_other_data(records):
    results = []

    for record in records:
        rdata = model.get_by_condition(
            table="rdata", field="record_id", value=record["id"]
        )
        zone = model.get_by_condition(table="zone", field="id", value=record["zone_id"])
        ttl = model.get_by_condition(table="ttl", field="id", value=record["ttl_id"])
        type_ = model.get_by_condition(
            table="type", field="id", value=record["type_id"]
        )

        data = {
            "id": record["id"],
            "owner": record["owner"],
            "rdata": rdata,
            "zone": zone,
            "type": type_,
            "ttl": ttl,
        }
        results.append(data)

    return results


def is_exists(record_id):
    record = model.get_by_condition(table="record", field="id", value=record_id)
    if not record:
        raise ValueError(f"Record Not Found")
