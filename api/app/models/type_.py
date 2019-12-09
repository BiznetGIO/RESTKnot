from app.models import model


def get_typeid_by_rtype(rtype):
    """Get type id by record record type."""
    try:
        type_ = model.get_by_condition(table="type", field="type", value=rtype.upper())
        type_id = type_[0]["id"]
        return type_id
    except Exception:
        raise ValueError("Unrecognized Record Type")


def get_type_by_recordid(record_id):
    """Get record type by record id."""
    try:
        record = model.get_by_condition(table="record", field="id", value=record_id)
        type_id = record[0]["type_id"]

        type_ = model.get_by_condition(table="type", field="id", value=type_id)
        return type_[0]["type"]
    except Exception:
        raise ValueError("Unrecognized Record Type")


def is_exists(type_id):
    type_ = model.get_by_condition(table="type", field="id", value=type_id)
    if not type_:
        raise ValueError(f"Type Not Found")
