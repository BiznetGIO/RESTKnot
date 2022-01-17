from typing import Any, Dict, List

from fastapi import APIRouter, HTTPException

from app.helpers import command, helpers, rules, validator
from app.models import record as record_db
from app.models import rtype as rtype_db
from app.models import ttl as ttl_db
from app.models import zone as zone_db
from app.schemas import Response
from app.schemas import record as schema

router = APIRouter()


def get_soa_record(zone_name) -> Dict:
    soa_record: Dict = {}

    zone = zone_db.get_by_name(zone_name)
    records = record_db.get_by_zone_id(zone["id"])

    for record in records:
        soa_type = rtype_db.get_by_value("SOA")
        soa_rtype_id = soa_type["id"]
        if record["rtype_id"] == soa_rtype_id:
            soa_record = record
            break

    return soa_record


def get_soa_serial(zone_name) -> str:
    soa_record = get_soa_record(zone_name)

    rdatas = soa_record["rdata"].split(" ")
    serial = rdatas[2]

    return serial


def check_serial_limit(serial: str):
    # `serial_counter` is the last two digit of serial value (YYYYMMDDnn)
    serial_counter = serial[-2:]
    serial_date = serial[:-2]

    today_date = helpers.soa_time_set()

    if int(serial_counter) > 97 and serial_date == today_date:
        # knot maximum of nn is 99
        # 97 was chosen because serial
        # increment can be twice at time
        raise ValueError("zone change limit reached")


def update_soa_serial(zone_name: str, increment: str = "01"):
    """Update serial in rdata"""

    soa_record = get_soa_record(zone_name)
    old_serial = get_soa_serial(zone_name)

    _new_serial = helpers.increment_serial(old_serial, increment)
    new_rdata = helpers.replace_serial(soa_record["rdata"], _new_serial)

    record_db.update(
        owner=soa_record["owner"],
        rdata=new_rdata,
        zone_id=soa_record["zone_id"],
        rtype_id=soa_record["rtype_id"],
        ttl_id=soa_record["ttl_id"],
        record_id=soa_record["id"],
    )


@router.get("/", response_model=Response[List[schema.Record]])
def read_all() -> Any:
    """
    Retrieve records.
    """
    records = record_db.get_all()

    records_detail = []
    for record in records:
        zone = zone_db.get(record["zone_id"])
        rtype = rtype_db.get(record["rtype_id"])
        ttl = ttl_db.get(record["ttl_id"])

        detail = {
            "id": record["id"],
            "owner": record["owner"],
            "rdata": record["rdata"],
            "zone": zone["zone"],
            "type": rtype["type"],
            "ttl": ttl["ttl"],
        }
        records_detail.append(detail)

    return Response(data=records_detail)


@router.get("/{record_id}", response_model=Response[schema.Record])
def read(record_id: int) -> Any:
    """
    Get a specific record by id.
    """
    record = record_db.get(record_id)
    if not record:
        raise HTTPException(status_code=404, detail="record not found")

    zone = zone_db.get(record["zone_id"])
    rtype = rtype_db.get(record["rtype_id"])
    ttl = ttl_db.get(record["ttl_id"])

    detail = {
        "id": record["id"],
        "owner": record["owner"],
        "rdata": record["rdata"],
        "zone": zone["zone"],
        "type": rtype["type"],
        "ttl": ttl["ttl"],
    }

    return Response(data=detail)


@router.post("/", response_model=Response[schema.Record], status_code=201)
def create(record_in: schema.RecordCreate) -> Any:
    """
    Create new record.
    """
    # Validate input
    ttl = ttl_db.get_by_value(record_in.ttl)
    if not ttl:
        raise HTTPException(
            status_code=400,
            detail="record with this email already exists in the system",
        )

    rtype = rtype_db.get_by_value(record_in.rtype)
    if not rtype:
        raise HTTPException(
            status_code=400,
            detail="record with this email already exists in the system",
        )

    zone = zone_db.get_by_name(record_in.zone)
    if not zone:
        raise HTTPException(
            status_code=400,
            detail="record with this email already exists in the system",
        )

    try:
        rules.check_add(
            rtype=record_in.rtype,
            zone_id=zone["id"],
            rtype_id=rtype["id"],
            owner=record_in.owner,
            rdata=record_in.rdata,
            ttl_id=ttl["id"],
        )
    except Exception as e:
        raise HTTPException(
            status_code=409,
            detail=f"{e}",
        )

    try:
        # rtype no need to be validated & no need to check its length
        # `get_typeid` will raise error for non existing rtype
        validator.validate(record_in.rtype, record_in.rdata)
        validator.validate("owner", record_in.owner)
    except Exception as e:
        raise HTTPException(
            status_code=422,
            detail=f"{e}",
        )

    try:
        serial = get_soa_serial(zone["zone"])
        check_serial_limit(serial)
    except Exception as e:
        raise HTTPException(
            status_code=429,
            detail=f"{e}",
        )

    record = record_db.add(
        owner=record_in.owner,
        rdata=record_in.rdata,
        zone_id=zone["id"],
        rtype_id=rtype["id"],
        ttl_id=ttl["id"],
    )
    if not record:
        raise ValueError("failed to store record")

    command.set_zone(record["id"], "zone-set")

    # increment serial after adding new record
    if rtype["rtype"] != "SOA":
        update_soa_serial(zone["zone"])

    updated_record = record_db.get(record["id"])
    if not updated_record:
        raise HTTPException(
            status_code=500,
            detail="failed to update record",
        )
    zone = zone_db.get(updated_record["zone_id"])
    rtype = rtype_db.get(updated_record["rtype_id"])
    ttl = ttl_db.get(updated_record["ttl_id"])

    result = {
        "id": updated_record["id"],
        "owner": updated_record["owner"],
        "rdata": updated_record["rdata"],
        "zone": zone["zone"],
        "rtype": rtype["rtype"],
        "ttl": ttl["ttl"],
    }
    return Response(data=result)


@router.put("/{record_id}", response_model=schema.Record)
def update(record_id: int, record_in: schema.RecordCreate) -> Any:
    """
    Update the record.
    """
    # Validate input
    ttl = ttl_db.get_by_value(record_in.ttl)
    if not ttl:
        raise HTTPException(
            status_code=400,
            detail="record with this email already exists in the system",
        )

    rtype = rtype_db.get_by_value(record_in.rtype)
    if not rtype:
        raise HTTPException(
            status_code=400,
            detail="record with this email already exists in the system",
        )

    zone = zone_db.get_by_name(record_in.zone)
    if not zone:
        raise HTTPException(
            status_code=400,
            detail="record with this email already exists in the system",
        )

    # Check rules
    try:
        rules.check_add(
            rtype=record_in.rtype,
            zone_id=zone["id"],
            rtype_id=rtype["id"],
            owner=record_in.owner,
            rdata=record_in.rdata,
            ttl_id=ttl["id"],
        )
    except Exception as e:
        raise HTTPException(
            status_code=409,
            detail=f"{e}",
        )

    try:
        # rtype no need to be validated & no need to check its length
        # `get_typeid` will raise error for non existing rtype
        validator.validate(rtype, record_in.rdata)
        validator.validate("owner", record_in.owner)
    except Exception as e:
        raise HTTPException(
            status_code=422,
            detail=f"{e}",
        )

    try:
        serial = get_soa_serial(zone["zone"])
        check_serial_limit(serial)
    except Exception as e:
        raise HTTPException(
            status_code=429,
            detail=f"{e}",
        )

    command.set_zone(record_id, "zone-unset")
    record = record_db.update(
        owner=record_in.owner,
        rdata=record_in.rdata,
        zone_id=zone["id"],
        rtype_id=rtype["id"],
        ttl_id=ttl["id"],
        record_id=record_id,
    )
    if not record:
        raise ValueError("failed to update record")

    command.set_zone(record_id, "zone-set")

    # increment serial after adding new record
    if rtype["rtype"] != "SOA":
        update_soa_serial(zone["zone"], "02")

    updated_record = record_db.get(record_id)
    zone = zone_db.get(updated_record["zone_id"])
    rtype = rtype_db.get(updated_record["rtype_id"])
    ttl = ttl_db.get(updated_record["ttl_id"])

    result = {
        "id": updated_record["id"],
        "owner": updated_record["owner"],
        "rdata": updated_record["rdata"],
        "zone": zone["zone"],
        "type": rtype["rtype"],
        "ttl": ttl["ttl"],
    }
    return result


@router.delete("/{record_id}", status_code=204)
def delete(record_id: int) -> Any:
    """
    Delete the record.
    """
    record = record_db.get(record_id)
    if not record:
        raise HTTPException(
            status_code=404,
            detail="record not found",
        )

    zone = zone_db.get(record["zone_id"])
    if not zone:
        raise HTTPException(
            status_code=404,
            detail="zone not found",
        )

    try:
        serial = get_soa_serial(zone["zone"])
        check_serial_limit(serial)
    except Exception as e:
        raise HTTPException(
            status_code=429,
            detail=f"{e}",
        )

    rtype = rtype_db.get(record["rtype_id"])
    if rtype["rtype"] == "SOA":
        raise HTTPException(
            status_code=403,
            detail="failed to delete SOA record",
        )
    if rtype["rtype"] != "SOA":
        update_soa_serial(zone["zone"])

    command.set_zone(record_id, "zone-unset")

    record_db.delete(record_id)
