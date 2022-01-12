from app.models import model


def get_typeid_by_rtype(rtype: str) -> int:
    """Get type id by record record type."""
    type_ = model.get_one(table="type", field="type", value=rtype.upper())
    if not type_:
        raise ValueError("Type Not Found")

    type_id = type_["id"]
    return type_id


def get_type_by_recordid(record_id: int) -> str:
    """Get record type by record id."""
    try:
        record = model.get_one(table="record", field="id", value=record_id)
        if not record:
            raise ValueError("Record Not Found")

        type_id = record["type_id"]

        type_ = model.get_one(table="type", field="id", value=type_id)
        if not type_:
            raise ValueError("Type Not Found")

        return type_["type"]
    except Exception:
        raise ValueError("Unrecognized Record Type")


def is_exists(type_id: int):
    type_ = model.get_one(table="type", field="id", value=type_id)
    if not type_:
        raise ValueError("Type Not Found")
