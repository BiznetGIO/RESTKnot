from app.models import model


class Rules:
    def __init__(self, query=None, value=None):
        """Append default query to given query."""
        self.query = (
            f'SELECT * FROM "record" WHERE "zone_id"=%(zone_id)s AND {query or None}'
        )
        self.value = value

    def is_unique(self):
        """Check if no record exists."""
        records = model.plain_get("record", self.query, self.value)

        if records:  # initial database will return None
            if len(records) == 0:
                return True
            return False

        return True  # also if None

    def is_coexist(self):
        """Check if no record exists."""
        records = model.plain_get("record", self.query, self.value)

        if records:
            if len(records) > 0:
                return True

        return False

    def is_duplicate(self, zone_id, type_id, owner, rdata):
        """Check duplicate record exists."""
        base_query = 'SELECT * FROM "record" WHERE "zone_id"=%(zone_id)s AND'
        query = base_query + '"type_id"=%(type_id)s AND "owner"=%(owner)s'
        value = {"zone_id": zone_id, "type_id": type_id, "owner": owner}

        records = model.plain_get("record", query, value)
        for record in records:
            rdata_record = model.get_one(
                table="rdata", field="record_id", value=record["id"]
            )
            if rdata == rdata_record["rdata"]:
                raise ValueError("The record already exists")
