from typing import Any, List, Optional

from fastapi import APIRouter, HTTPException

from app.core.config import settings
from app.helpers import command, helpers, validator
from app.models import record as record_db
from app.models import rtype as rtype_db
from app.models import ttl as ttl_db
from app.models import user as user_db
from app.models import zone as zone_db
from app.schemas import Response
from app.schemas import domain as schema

router = APIRouter()


def get_soa_rdata() -> str:
    """Get SOA rdata.

    Notes:
    <MNAME> <RNAME> <serial> <refresh> <retry> <expire> <minimum>
    See: https://tools.ietf.org/html/rfc1035 (3.3.13. SOA RDATA format)
    """
    current_time = helpers.soa_time_set()
    serial = f"{str(current_time)}01"
    default_soa_content = settings.DEFAULT_SOA_RDATA
    rdatas = default_soa_content.split(" ")
    # rdata doesn't contains serial
    mname_and_rname = " ".join(rdatas[0:2])
    ttls = " ".join(rdatas[2:])

    rdata = f"{mname_and_rname} {serial} {ttls}"
    return rdata


def add_soa_record(zone_id: int):
    """Add default SOA record"""
    rdata = get_soa_rdata()
    record = record_db.add(
        owner="@", rdata=rdata, zone_id=zone_id, rtype_id=1, ttl_id=6
    )
    if not record:
        raise ValueError("failed to store record")

    command.set_zone(record["id"], "zone-set")


def add_ns_record(zone_id: int):
    """Add default NS record"""
    # default NS must be present
    default_ns = settings.DEFAULT_NS
    nameservers = default_ns.split(" ")

    for nameserver in nameservers:
        record = record_db.add(
            owner="@", rdata=nameserver, zone_id=zone_id, rtype_id=4, ttl_id=6
        )
        if not record:
            raise ValueError("failed to store record")

        command.set_zone(record["id"], "zone-set")


def add_cname_record(zone_id: int, zone_name: str):
    """Add default CNAME record"""
    record = record_db.add(
        owner="www", rdata=f"{zone_name}.", zone_id=zone_id, rtype_id=5, ttl_id=6
    )
    if not record:
        raise ValueError("failed to store record")

    command.set_zone(record["id"], "zone-set")


@router.get("/", response_model=Response[List[schema.Domain]])
def read_all() -> Any:
    """
    Retrieve domains.
    """
    zones = zone_db.get_all()
    if not zones:
        raise HTTPException(status_code=404, detail="zone not found")

    results = []
    for zone in zones:
        records = record_db.get_by_zone_id(zone["id"])
        user  = user_db.get(zone["user_id"])

        _result = {
            "zone_id": zone["id"],
            "zone": zone["zone"],
            "user": user,
            "records": records,
        }
        results.append(_result)

    return Response(data=results)


@router.get("/{zone_id}", response_model=Response[schema.Domain])
def read(zone_id: int) -> Any:
    """
    Get a specific domain by id.
    """
    zone = zone_db.get(zone_id)
    if not zone:
        raise HTTPException(status_code=404, detail="zone not found")

    records = record_db.get_by_zone_id(zone["id"])
    result = {"zone": zone["zone"], "records": records}
    return Response(data=result)


@router.get("/zone/{zone_name}", response_model=Response[schema.Domain])
def read_by_zone_name(zone_name: str) -> Any:
    """
    Get a specific domain by id.
    """
    zone = zone_db.get_by_name(zone_name)
    if not zone:
        raise HTTPException(status_code=404, detail="zone not found")

    records = record_db.get_by_zone_id(zone["id"])
    result = {"zone": zone["zone"], "records": records}
    return Response(data=result)


@router.get("/user/{user_id}", response_model=Response[schema.Domain])
def read_by_user_id(user_id: int) -> Any:
    """
    Get a specific domain by id.
    """
    zones = zone_db.get_by_user_id(user_id)
    if not zones:
        raise HTTPException(
            status_code=404,
            detail="zone not found",
        )

    zone_details = []
    for zone in zones:
        records = record_db.get_by_zone_id(zone["id"])

        records_details = []
        for record in records:
            rtype = rtype_db.get(record["rtype_id"])
            ttl = ttl_db.get(record["ttl_id"])

            record_detail = {
                "id": record["id"],
                "owner": record["owner"],
                "rdata": record["rdata"],
                "zone": zone["zone"],
                "rtype": rtype["rtype"],
                "ttl": ttl["ttl"],
            }
            records_details.append(record_detail)

        zone_detail = {"zone": zone["zone"], "records": records_details}
        zone_details.append(zone_detail)

    return Response(data=zone_details)


@router.post("/", response_model=Response[schema.Domain], status_code=201)
def create(domain_in: schema.DomainCreate) -> Any:
    """
    Create new domain.
    """
    _zone = zone_db.get_by_name(domain_in.zone)
    if _zone:
        raise HTTPException(
            status_code=409,
            detail="zone already exists",
        )

    _user = user_db.get(domain_in.user_id)
    if not _user:
        raise HTTPException(
            status_code=404,
            detail="user not found",
        )

    # Validation
    try:
        validator.validate("ZONE", domain_in.zone)
    except Exception as e:
        raise HTTPException(
            status_code=422,
            detail=f"{e}",
        )

    new_zone: Optional[Any] = zone_db.add(domain_in.zone, domain_in.user_id)
    zone_id: int = new_zone["id"]

    # Create zone configurations in agents
    command.set_config(domain_in.zone, "conf-set")

    # Create default records in db and agents
    add_soa_record(zone_id)
    add_ns_record(zone_id)
    add_cname_record(zone_id, domain_in.zone)

    command.delegate(domain_in.zone, "conf-set", "master")
    command.delegate(domain_in.zone, "conf-set", "slave")

    result = {"id": zone_id, "zone": domain_in.zone}
    return Response(data=result)


@router.delete("/zone/{zone_name}", status_code=204)
def delete_by_zone_name(zone_name: str) -> Any:
    """
    Delete the domain.
    """
    zone = zone_db.get_by_name(zone_name)
    if not zone:
        raise HTTPException(
            status_code=404,
            detail="zone not found",
        )

    records = record_db.get_by_zone_id(zone["id"])
    for record in records:
        # zone-purge didn't work
        # all the records must be unset one-by-one. otherwise old record
        # will appear again if the same zone name crated.
        command.set_zone(record["id"], "zone-unset")

    command.set_config(zone_name, "conf-unset")

    # other data (e.g record) deleted automatically
    # by cockroach when no PK existed
    zone_db.delete(zone["id"])
