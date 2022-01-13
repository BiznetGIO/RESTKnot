import os
from typing import Any, Optional

from flask import Response, current_app, request
from flask_restful import Resource, reqparse

from app.helpers import command, helpers, producer, validator
from app.helpers.rest import response
from app.middlewares import auth
from app.models import record as record_db
from app.models import ttl as ttl_db
from app.models import type_ as type_db
from app.models import user as user_db
from app.models import zone as zone_db


def get_soa_rdata() -> str:
    """Get SOA rdata.

    Notes:
    <MNAME> <RNAME> <serial> <refresh> <retry> <expire> <minimum>
    See: https://tools.ietf.org/html/rfc1035 (3.3.13. SOA RDATA format)
    """
    current_time = helpers.soa_time_set()
    serial = f"{str(current_time)}01"
    default_soa_content = os.environ.get("DEFAULT_SOA_RDATA", "")
    rdatas = default_soa_content.split(" ")
    # rdata doesn't contains serial
    mname_and_rname = " ".join(rdatas[0:2])
    ttls = " ".join(rdatas[2:])

    rdata = f"{mname_and_rname} {serial} {ttls}"
    return rdata


def add_soa_record(zone_id: int):
    """Add default SOA record"""
    rdata = get_soa_rdata()
    record = record_db.add(owner="@", rdata=rdata, zone_id=zone_id, type_id=1, ttl_id=6)
    if not record:
        raise ValueError("failed to store record")

    command.set_zone(record["id"], "zone-set")


def add_ns_record(zone_id: int):
    """Add default NS record"""
    # default NS must be present
    default_ns = os.environ["DEFAULT_NS"]
    nameservers = default_ns.split(" ")

    for nameserver in nameservers:
        record = record_db.add(
            owner="@", rdata=nameserver, zone_id=zone_id, type_id=4, ttl_id=6
        )
        if not record:
            raise ValueError("failed to store record")

        command.set_zone(record["id"], "zone-set")


def add_cname_record(zone_id: int, zone_name: str):
    """Add default CNAME record"""
    record = record_db.add(
        owner="www", rdata=f"{zone_name}.", zone_id=zone_id, type_id=5, ttl_id=6
    )
    if not record:
        raise ValueError("failed to store record")

    command.set_zone(record["id"], "zone-set")


class GetDomainData(Resource):
    @auth.auth_required
    def get(self) -> Response:
        try:
            zones = zone_db.get_all()
            if not zones:
                return response(404)

            results = []
            for zone in zones:
                records = record_db.get_by_zone_id(zone["id"])
                if not records:
                    return response(404, message="records not found")

                user = user_db.get(zone["user_id"])
                if not user:
                    return response(404, message="user not found")

                _result = {
                    "zone_id": zone["id"],
                    "zone": zone["zone"],
                    "user": user,
                    "records": records,
                }
                results.append(_result)

            return response(200, data=results)
        except Exception as e:
            current_app.logger.error(f"{e}")
            return response(500)


class GetDomainDataId(Resource):
    @auth.auth_required
    def get(self) -> Response:
        zone_id = request.args.get("id")
        zone_name = request.args.get("name")

        if not any((zone_id, zone_name)):
            return response(422, "problems parsing parameters")

        try:
            if zone_id:
                zone = zone_db.get(int(zone_id))
                if not zone:
                    return response(404, message="zone not found")

            if zone_name:
                zone = zone_db.get_by_name(zone_name)
                if not zone:
                    return response(404, message="zone not found")

            if not zone:
                return response(404)

            records = record_db.get_by_zone_id(zone["id"])
            if not records:
                return response(404, message="records not found")

            zone_name = zone["zone"]
            result = {"zone": zone_name, "records": records}
            return response(200, data=result)
        except Exception as e:
            current_app.logger.error(f"{e}")
            return response(500)


class GetDomainByUser(Resource):
    @auth.auth_required
    def get(self, user_id: int) -> Response:
        try:
            zones = zone_db.get_by_user_id(user_id)
            if not zones:
                return response(404, message="zone not found")

            zone_details = []
            for zone in zones:
                records = record_db.get_by_zone_id(zone["id"])
                if not records:
                    return response(404, message="records not found")

                records_details = []
                for record in records:
                    type_ = type_db.get(record["type_id"])
                    if not type_:
                        return response(404, message="type not found")

                    ttl = ttl_db.get(record["ttl_id"])
                    if not ttl:
                        return response(404, message="ttl not found")

                    record_detail = {
                        "id": record["id"],
                        "owner": record["owner"],
                        "rdata": record["rdata"],
                        "zone": zone["zone"],
                        "type": type_["type"],
                        "ttl": ttl["ttl"],
                    }
                    records_details.append(record_detail)

                zone_detail = {"zone": zone["zone"], "records": records_details}
                zone_details.append(zone_detail)

            return response(200, data=zone_details)
        except Exception as e:
            current_app.logger.error(f"{e}")
            return response(500)


class AddDomain(Resource):
    @producer.check_producer
    @auth.auth_required
    def post(self) -> Response:
        """Add new domain (zone) with additional default record.

        note:
        SOA, NS, and CNAME records are added automatically when adding new domain
        """
        parser = reqparse.RequestParser()
        parser.add_argument("zone", type=str, required=True)
        parser.add_argument("user_id", type=int, required=True)
        args = parser.parse_args()
        # zone_name and domain_name are interchangeable
        zone_name = args["zone"]
        user_id = args["user_id"]

        _zone = zone_db.get_by_name(zone_name)
        if _zone:
            return response(409, message="zone already exists")

        _user = user_db.get(user_id)
        if not _user:
            return response(404, message="user not found")

        # Validation
        try:
            validator.validate("ZONE", zone_name)
        except Exception as e:
            return response(422, message=f"{e}")

        try:
            new_zone: Optional[Any] = zone_db.add(zone_name, user_id)
            if not new_zone:
                raise ValueError("failed to store zone")
            zone_id: int = new_zone["id"]

            # Create zone configurations in agents
            command.set_config(zone_name, "conf-set")

            # Create default records in db and agents
            add_soa_record(zone_id)
            add_ns_record(zone_id)
            add_cname_record(zone_id, zone_name)

            command.delegate(zone_name, "conf-set", "master")
            command.delegate(zone_name, "conf-set", "slave")

            data_ = {"id": zone_id, "zone": zone_name}
            return response(201, data=data_)
        except Exception as e:
            current_app.logger.error(f"{e}")
            return response(500)


class DeleteDomain(Resource):
    @producer.check_producer
    @auth.auth_required
    def delete(self) -> Response:
        """Remove domain (zone) and all its related records."""
        parser = reqparse.RequestParser()
        parser.add_argument("zone", type=str, required=True)
        args = parser.parse_args()
        zone_name = args["zone"]

        zone = zone_db.get_by_name(zone_name)
        if not zone:
            return response(404, message="zone not found")

        try:
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

            return response(204)
        except Exception as e:
            current_app.logger.error(f"{e}")
            return response(500)
