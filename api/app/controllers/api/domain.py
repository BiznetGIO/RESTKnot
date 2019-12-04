import os
from flask_restful import Resource, reqparse

from app.helpers.rest import response
from app.models import model
from app.models import zone as zone_model
from app.libs import utils
from app.libs import validation
from app.helpers import command
from app.helpers import producer
from app.middlewares import auth


def insert_zone(zone, project_id):

    user = model.get_by_condition(
        table="user", field="project_id", value=f"{project_id}"
    )
    user_id = user[0]["id"]

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
    serial = utils.soa_time_set() + "01"
    default_soa_content = os.environ.get("DEFAULT_SOA_RDATA")
    rdatas = default_soa_content.split(" ")
    mname_and_rname = " ".join(rdatas[0:2])
    ttls = " ".join(rdatas[2:])

    rdata = f"{mname_and_rname} {serial} {ttls}"
    content_data = {"rdata": rdata, "record_id": record_id}

    model.insert(table="rdata", data=content_data)


def insert_soa(zone_id):
    """Insert default SOA record"""
    record_id = insert_soa_record(zone_id)
    insert_soa_rdata(record_id)
    return record_id


def insert_ns_record(zone_id):
    record_data = {"owner": "@", "zone_id": zone_id, "type_id": "4", "ttl_id": "6"}
    record_id = model.insert(table="record", data=record_data)
    return record_id


def insert_ns_rdata(record_id):
    default_ns = os.environ.get("DEFAULT_NS")
    nameserver = default_ns.split(" ")

    for name in nameserver:
        data = {"rdata": name, "record_id": record_id}
        model.insert(table="rdata", data=data)


def insert_ns(zone_id):
    record_id = insert_ns_record(zone_id)
    insert_ns_rdata(record_id)
    return record_id


def insert_cname_record(zone_id):
    record_data = {"owner": "www", "zone_id": zone_id, "type_id": "5", "ttl_id": "6"}
    record_id = model.insert(table="record", data=record_data)
    return record_id


def insert_cname_rdata(zone, record_id):
    data = {"rdata": f"{zone}.", "record_id": record_id}
    model.insert(table="rdata", data=data)


def insert_cname(zone_id, zone):
    record_id = insert_cname_record(zone_id)
    insert_cname_rdata(zone, record_id)
    return record_id


def get_record_datum(data):
    if data is None:
        return

    results = []
    for d in data:
        datum = {
            "id": str(d["id"]),
            "owner": d["owner"],
            "type_id": d["type_id"],
            "ttl_id": d["ttl_id"],
        }
        results.append(datum)
    return results


def get_user_datum(data):
    if data is None:
        return

    results = []
    for d in data:
        datum = {"id": str(d["id"]), "email": d["email"], "project_id": d["project_id"]}
        results.append(datum)
    return results


def get_datum(data):
    if data is None:
        return

    results = []
    for d in data:
        user = model.get_by_condition(table="user", field="id", value=d["user_id"])
        record = model.get_by_condition(table="record", field="zone_id", value=d["id"])
        user_datum = get_user_datum(user)
        record_datum = get_record_datum(record)

        datum = {
            "zone_id": d["id"],
            "zone": d["zone"],
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

        data = get_datum(zones)
        return response(200, data=data)


class GetDomainDataId(Resource):
    @auth.auth_required
    def get(self, zone_id):
        try:
            zone = model.get_by_condition(table="zone", field="id", value=zone_id)
        except Exception as e:
            return response(401, message=str(e))
        else:
            data = get_datum(zone)
            return response(200, data=data)


class GetDomainDataByProjectId(Resource):
    @auth.auth_required
    def get(self, project_id):

        try:
            user = model.get_by_condition(
                table="user", field="project_id", value=f"{project_id}"
            )
            user_id = user[0]["id"]
            zone = model.get_by_condition(table="zone", field="user_id", value=user_id)
        except Exception as e:
            return response(401, message=str(e))
        else:
            data = get_datum(zone)
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
        if validation.zone_validation(zone):
            return response(401, message="Named Error")

        try:
            zone_id = insert_zone(zone, project_id)
        except Exception:
            return response(401, message="Project ID not found")
        else:
            # add zone config
            command.send_config(zone, zone_id, "conf-set")

            soa_record_id = insert_soa(zone_id)
            ns_record_id = insert_ns(zone_id)
            cname_record_id = insert_cname(zone_id, zone)
            command.send_zone(soa_record_id, "zone-set")
            command.send_zone(ns_record_id, "zone-set")
            command.send_zone(cname_record_id, "zone-set")

            try:
                command.cluster_command(cname_record_id)
            except Exception as e:
                return response(401, message=str(e))

            # just for feedback return value
            zone_data = {"zone": zone, "project_id": project_id}
            return response(200, data=zone_data, message="Inserted")
