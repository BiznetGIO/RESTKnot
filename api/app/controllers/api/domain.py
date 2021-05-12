import os

from flask import current_app, request
from flask_restful import Resource, reqparse

from app.helpers import command, helpers, validator
from app.middlewares import auth
from app.models import domain as domain_model
from app.models import model
from app.models import record as record_model
from app.models import zone as zone_model
from app.vendors.rest import response


def insert_zone(zone, user_id):
    data = {"zone": zone, "user_id": user_id}
    zone_id = model.insert(table="zone", data=data)
    return zone_id


def insert_soa_record(zone_id):
    record_data = {"owner": "@", "zone_id": zone_id, "type_id": "1", "ttl_id": "6"}
    record_id = model.insert(table="record", data=record_data)
    return record_id


def insert_soa_rdata(record_id):
    """Insert default SOA record.

    Notes:
    <MNAME> <RNAME> <serial> <refresh> <retry> <expire> <minimum>
    See: https://tools.ietf.org/html/rfc1035 (3.3.13. SOA RDATA format)
    """
    current_time = helpers.soa_time_set()
    serial = f"{str(current_time)}01"
    default_soa_content = os.environ.get("DEFAULT_SOA_RDATA")
    rdatas = default_soa_content.split(" ")
    # rdata doesn't contains serial
    mname_and_rname = " ".join(rdatas[0:2])
    ttls = " ".join(rdatas[2:])

    rdata = f"{mname_and_rname} {serial} {ttls}"
    content_data = {"rdata": rdata, "record_id": record_id}

    model.insert(table="rdata", data=content_data)


def insert_soa_default(zone_id):
    """Create default SOA record"""
    record_id = insert_soa_record(zone_id)
    insert_soa_rdata(record_id)
    return record_id


def insert_ns_record(zone_id):
    record_data = {"owner": "@", "zone_id": zone_id, "type_id": "4", "ttl_id": "6"}
    record_id = model.insert(table="record", data=record_data)
    return record_id


def insert_ns_rdata(name, record_id):
    data = {"rdata": name, "record_id": record_id}
    model.insert(table="rdata", data=data)


def insert_ns_default(zone_id):
    """Create default NS record"""
    default_ns = os.environ.get("DEFAULT_NS")
    nameserver = default_ns.split(" ")
    record_ids = []

    for name in nameserver:
        record_id = insert_ns_record(zone_id)
        insert_ns_rdata(name, record_id)
        record_ids.append(record_id)

    return record_ids


def insert_cname_record(zone_id):
    record_data = {"owner": "www", "zone_id": zone_id, "type_id": "5", "ttl_id": "6"}
    record_id = model.insert(table="record", data=record_data)
    return record_id


def insert_cname_rdata(zone, record_id):
    data = {"rdata": f"{zone}.", "record_id": record_id}
    model.insert(table="rdata", data=data)


def insert_cname_default(zone_id, zone):
    """Create default CNAME record"""
    record_id = insert_cname_record(zone_id)
    insert_cname_rdata(zone, record_id)
    return record_id


class GetDomainData(Resource):
    @auth.auth_required
    def get(self):
        try:
            zones = model.get_all("zone")
            if not zones:
                return response(404)

            domains_detail = []
            for zone in zones:
                detail = domain_model.get_other_data(zone)
                domains_detail.append(detail)

            return response(200, data=domains_detail)
        except Exception as e:
            current_app.logger.error(f"{e}")
            return response(500)


class GetDomainDataId(Resource):
    @auth.auth_required
    def get(self):
        zone_id = request.args.get("id")
        zone_name = request.args.get("name")

        if not any((zone_id, zone_name)):
            return response(422, "Problems parsing parameters")

        try:
            if zone_id:
                zone = model.get_one(table="zone", field="id", value=zone_id)

            if zone_name:
                zone = model.get_one(table="zone", field="zone", value=zone_name)

            if not zone:
                return response(404)

            data = domain_model.get_other_data(zone)
            return response(200, data=data)
        except Exception as e:
            current_app.logger.error(f"{e}")
            return response(500)


class GetDomainByUser(Resource):
    @auth.auth_required
    def get(self, user_id):
        try:
            zones = zone_model.get_zones_by_user(user_id)
            if not zones:
                return response(404)

            domains_detail = []
            for zone in zones:
                detail = domain_model.get_other_data(zone)
                domains_detail.append(detail)

            return response(200, data=domains_detail)
        except Exception as e:
            current_app.logger.error(f"{e}")
            return response(500)


class AddDomain(Resource):
    @helpers.check_producer
    @auth.auth_required
    def post(self):
        """Add new domain (zone) with additional default record.

        note:
        SOA, NS, and CNAME records are added automatically when adding new domain
        """
        parser = reqparse.RequestParser()
        parser.add_argument("zone", type=str, required=True)
        parser.add_argument("user_id", type=int, required=True)
        args = parser.parse_args()
        zone = args["zone"]
        user_id = args["user_id"]

        # Validation
        if not model.is_unique(table="zone", field="zone", value=f"{zone}"):
            return response(409, message="Duplicate Zone")

        user = model.get_one(table="user", field="id", value=user_id)
        if not user:
            return response(404, message="User Not Found")

        try:
            validator.validate("ZONE", zone)
        except Exception as e:
            return response(422, message=f"{e}")

        try:
            zone_id = insert_zone(zone, user_id)

            # create zone config
            command.set_config(zone, zone_id, "conf-set")

            # create default records
            soa_record_id = insert_soa_default(zone_id)
            ns_record_ids = insert_ns_default(zone_id)
            cname_record_id = insert_cname_default(zone_id, zone)
            record_ids = [soa_record_id, *ns_record_ids, cname_record_id]
            command.set_default_zone(record_ids)

            command.delegate(zone, zone_id, "conf-set", "master")
            command.delegate(zone, zone_id, "conf-set", "slave")

            data_ = {"id": zone_id, "zone": zone}
            return response(201, data=data_)
        except Exception as e:
            current_app.logger.error(f"{e}")
            return response(500)


class DeleteDomain(Resource):
    @helpers.check_producer
    @auth.auth_required
    def delete(self):
        """Remove domain (zone) and all its related records."""
        parser = reqparse.RequestParser()
        parser.add_argument("zone", type=str, required=True)
        args = parser.parse_args()
        zone = args["zone"]

        try:
            zone_id = zone_model.get_zone_id(zone)
        except Exception:
            return response(404, message="Zone Not Found")

        try:
            records = record_model.get_records_by_zone(zone)
            for record in records:
                # zone-purge didn't work
                # all the records must be unset one-by-one. otherwise old record
                # will appear again if the same zone name crated.
                command.set_zone(record["id"], "zone-unset")
            command.set_config(zone, zone_id, "conf-unset")

            # other data (e.g record) deleted automatically
            # by cockroach when no PK existed
            model.delete(table="zone", field="id", value=zone_id)

            return response(204, data=zone)
        except Exception as e:
            current_app.logger.error(f"{e}")
            return response(500)
