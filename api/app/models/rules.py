from app.models import model


class Rules:
    def __init__(self, query, value):
        self.query = 'SELECT * FROM "record" WHERE "zone_id"=%(zone_id)s AND' + query
        self.value = value

    def is_unique(self):
        records = model.plain_get("record", self.query, self.value)

        if records:  # initial database will return None
            if len(records) == 0:
                return True
            return False

        return True  # also if None

    def is_coexist(self):
        records = model.plain_get("record", self.query, self.value)

        if records:
            if len(records) > 0:
                return True

        return False
