import os
from flask_restful import Resource, reqparse

from app.helpers.rest import response
from app.models import model
from app.models import zone as zone_model
from app.models import user as user_model
from app.models import record as record_model
from app.helpers import helpers
from app.helpers import validator
from app.helpers import command
from app.middlewares import auth


def insert_zone(zone, project_id):
    user_id = user_model.user_id_by_project(project_id)

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
    serial = helpers.soa_time_set() + "01"
    default_soa_content = os.environ.get("DEFAULT_SOA_RDATA")
    rdatas = default_soa_content.split(" ")
    mname_and_rname = " ".join(rdatas[0:2])
    ttls = " ".join(rdatas[2:])

    rdata = f"{mname_and_rname} {serial} {ttls}"
    content_data = {"rdata": rdata, "record_id": record_id}

    model.insert(table="rdata", data=content_data)


def create_soa_default(zone_id):
    """Create default SOA record"""
    record_id = insert_soa_record(zone_id)
    insert_soa_rdata(record_id)
    command.send_zone(record_id, "zone-set")


def insert_ns_record(zone_id):
    record_data = {"owner": "@", "zone_id": zone_id, "type_id": "4", "ttl_id": "6"}
    record_id = model.insert(table="record", data=record_data)
    return record_id


def insert_ns_rdata(name, record_id):
    data = {"rdata": name, "record_id": record_id}
    model.insert(table="rdata", data=data)


def create_ns_default(zone_id):
    """Create default NS record"""
    default_ns = os.environ.get("DEFAULT_NS")
    nameserver = default_ns.split(" ")

    for name in nameserver:
        record_id = insert_ns_record(zone_id)
        insert_ns_rdata(name, record_id)
        command.send_zone(record_id, "zone-set")


def insert_cname_record(zone_id):
    record_data = {"owner": "www", "zone_id": zone_id, "type_id": "5", "ttl_id": "6"}
    record_id = model.insert(table="record", data=record_data)
    return record_id


def insert_cname_rdata(zone, record_id):
    data = {"rdata": f"{zone}.", "record_id": record_id}
    model.insert(table="rdata", data=data)


def create_cname_default(zone_id, zone):
    record_id = insert_cname_record(zone_id)
    insert_cname_rdata(zone, record_id)
    command.send_zone(record_id, "zone-set")
    return record_id


def get_other_data(zones):
    results = []

    if zones is None:
        return

    for zone in zones:
        users = model.get_by_condition(table="user", field="id", value=zone["user_id"])
        records = model.get_by_condition(
            table="record", field="zone_id", value=zone["id"]
        )
        user_datum = user_model.get_datum(users)
        record_datum = record_model.get_other_data(records)

        datum = {
            "zone_id": zone["id"],
            "zone": zone["zone"],
            "user": user_datum,
            "record": record_datum,
        }
        results.append(datum)
    return results


class GetDomainData(Resource):
    @auth.auth_required
    def get(self):
        try:
            zones = model.get_all("zone")
        except Exception as e:
            return response(401, message=str(e))

        data = get_other_data(zones)
        return response(200, data=data)


class GetDomainDataId(Resource):
    @auth.auth_required
    def get(self, zone_id):
        try:
            zones = model.get_by_condition(table="zone", field="id", value=zone_id)
        except Exception as e:
            return response(401, message=str(e))
        else:
            data = get_other_data(zones)
            return response(200, data=data)


class GetDomainDataByProjectId(Resource):
    @auth.auth_required
    def get(self, project_id):

        try:
            user_id = user_model.user_id_by_project(project_id)

            zones = model.get_by_condition(table="zone", field="user_id", value=user_id)
        except Exception as e:
            return response(401, message=str(e))
        else:
            data = get_other_data(zones)
            return response(200, data=data)


class DeleteDomain(Resource):
    def get_record_ids(self, records):
        soa_record_id = None
        ns_record_id = None
        cname_record_id = None

        for item in records:
            if item.get("type_id") == 1:
                soa_record_id = item.get("id")
            if item.get("type_id") == 4:
                ns_record_id = item.get("id")
            if item.get("type_id") == 5:
                cname_record_id = item.get("id")
        return soa_record_id, ns_record_id, cname_record_id

    @auth.auth_required
    def delete(self):
        parser = reqparse.RequestParser()
        parser.add_argument("zone", type=str, required=True)
        args = parser.parse_args()
        zone = args["zone"]

        try:
            zone_id = zone_model.get_zone_id(zone)
            records = model.get_by_condition(
                table="record", field="zone_id", value=zone_id
            )
            soa_record_id, ns_record_id, cname_record_id = self.get_record_ids(records)

            # unset conf
            command.send_config(zone, zone_id, "conf-unset")
            # unset zone
            command.send_zone(soa_record_id, "zone-unset")
            command.send_zone(ns_record_id, "zone-unset")
            command.send_zone(cname_record_id, "zone-unset")
            # no need to perform unset for clusering, the necessary file deleted
            # automatically after the above operation

            # other data (e.g record) deleted automatically
            # by cockroach when no PK existed
            model.delete(table="zone", field="id", value=zone_id)

            return response(200, data=zone, message="Deleted")
        except IndexError:
            return response(401, message=f"Zone Not Found")
        except Exception as e:
            return response(401, message=str(e))


class AddDomain(Resource):
    @auth.auth_required
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("zone", type=str, required=True)
        parser.add_argument("project_id", type=str, required=True)
        args = parser.parse_args()
        zone = args["zone"]
        project_id = args["project_id"]

        # Validation
        if not model.is_unique(table="zone", field="zone", value=f"{zone}"):
            return response(401, message="Duplicate zone Detected")

        try:
            validator.validate("ZONE", zone)
        except Exception as e:
            return response(401, message=str(e))

        try:
            zone_id = insert_zone(zone, project_id)
        except Exception:
            return response(401, message="Project ID not found")
        else:
            # create zone config
            command.send_config(zone, zone_id, "conf-set")

            # create default records
            create_soa_default(zone_id)
            create_ns_default(zone_id)
            create_cname_default(zone_id, zone)

            try:
                command.send_cluster(zone_id)
            except Exception as e:
                return response(401, message=str(e))

            # just for feedback return value
            zone_data = {"zone": zone, "project_id": project_id}
            return response(200, data=zone_data, message="Inserted")
