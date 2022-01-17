from app.models import connect


class Rules:
    def is_unique(self, query: str) -> bool:
        """Check if no record exists."""
        cursor, _ = connect()

        cursor.execute(query, prepare=True)
        records = cursor.fetchall()

        if records:  # initial database will return None
            if len(records) == 0:
                return True
            return False

        return True  # also if None

    def is_coexist(self, query: str) -> bool:
        """Check if no record exists."""
        cursor, _ = connect()

        cursor.execute(query, prepare=True)
        records = cursor.fetchall()

        if records:
            if len(records) > 0:
                return True

        return False

    def is_duplicate(
        self, zone_id: int, rtype_id: int, owner: str, rdata: str, ttl_id: int
    ):
        """Check duplicate record exists."""
        cursor, _ = connect()

        query = f""" SELECT * FROM "record" WHERE "owner" = '{owner}' AND "zone_id" = {zone_id} AND "rtype_id" = {rtype_id} AND "ttl_id" = {ttl_id}  """
        cursor.execute(query, prepare=True)
        records = cursor.fetchall()

        for record in records:
            if not record["rdata"]:
                raise ValueError("Rdata Not Found")

            if rdata == record["rdata"]:
                raise ValueError("record already exists")
