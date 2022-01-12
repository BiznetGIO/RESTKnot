from app.models import model


def is_exists(ttl_id: int):
    ttl_ = model.get_one(table="ttl", field="id", value=ttl_id)
    if not ttl_:
        raise ValueError("TTL Not Found")


def get_ttlid_by_ttl(ttl: str):
    """Get type id by record record type."""
    ttl_ = model.get_one(table="ttl", field="ttl", value=ttl)
    if not ttl_:
        raise ValueError("TTL Not Found")

    ttl_id = ttl_["id"]
    return ttl_id
