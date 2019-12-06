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


def is_duplicate_rdata(zone_id, type_id, rdata):
    query = (
        'SELECT * FROM "record" WHERE "zone_id"=%(zone_id)s AND "type_id"=%(type_id)s'
    )
    value = {"zone_id": zone_id, "type_id": type_id}
    records = model.plain_get("record", query, value)
    for record in records:
        rdatas = model.get_by_condition(
            table="rdata", field="record_id", value=record["id"]
        )
        if rdata == rdatas[0]["rdata"]:
            raise ValueError(f"Can't Have Multiple Record with Same Content")
