from app.models import model


def is_exists(ttl_id):
    ttl_ = model.get_one(table="ttl", field="id", value=ttl_id)
    if not ttl_:
        raise ValueError(f"TTL Not Found")
