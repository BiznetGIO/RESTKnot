import os
from flask_restful import Resource, reqparse

from app.helpers.rest import response
from app.models import model
from app.libs import utils
from app.libs import validation
from app.helpers import command
from app.helpers import producer
from app.middlewares import auth


def insert_zone(zone, project_id):

    user = model.get_by_id(table="user", field="project_id", id_=f"'{project_id}'")
    user_id = user[0]["id"]

    data = {"zone": zone, "user_id": user_id}
    zone_id = model.insert(table="zone", data=data)
    return zone_id


def insert_soa_record(zone_id):
    record_data = {
        "record": "@",
        "is_serial": False,
        "zone_id": zone_id,
        "type_id": "1",
        "ttl_id": "6",
    }
    record_id = model.insert(table="record", data=record_data)
    return record_id


def insert_record_content(record_id):
    date_data = utils.soa_time_set() + "01"
    default_soa_content = os.environ.get("DEFAULT_SOA_CONTENT")
    default_soa_serial = os.environ.get("DEFAULT_SOA_SERIAL")

    content = f"{default_soa_content} {date_data} {default_soa_serial}"
    content_data = {"content": content, "record_id": record_id}

    model.insert(table="content", data=content_data)


def insert_soa_default(zone_id):
    record_id = insert_soa_record(zone_id)
    insert_record_content(record_id)
    return record_id


def insert_ns_record(zone_id):
    record_data = {
        "record": "@",
        "is_serial": False,
        "zone_id": zone_id,
        "type_id": "4",
        "ttl_id": "6",
    }
    record_id = model.insert(table="record", data=record_data)
    return record_id


def insert_ns_content(record_id):
    default_ns = os.environ.get("DEFAULT_NS")
    nameserver = default_ns.split(" ")

    for name in nameserver:
        content_data = {"content": name, "record_id": record_id}
        model.insert(table="content", data=content_data)


def insert_ns_default(zone_id):
    record_id = insert_ns_record(zone_id)
    insert_ns_content(record_id)
    return record_id


def insert_cname_record(zone_id):
    record_data = {
        "record": "www",
        "is_serial": False,
        "zone_id": zone_id,
        "type_id": "5",
        "ttl_id": "6",
    }
    record_id = model.insert(table="record", data=record_data)
    return record_id


def insert_cname_content(zone, record_id):
    content_data = {"content": f"{zone}.", "record_id": record_id}
    model.insert(table="content", data=content_data)


def insert_cname(zone_id, zone):
    record_id = insert_cname_record(zone_id)
    insert_cname_content(zone, record_id)
    return record_id


def get_record_datum(data):
    if data is None:
        return

    results = []
    for d in data:
        datum = {
            "id": str(d["id"]),
            "record": d["record"],
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
        user = model.get_by_id(table="user", field="id", id_=d["user_id"])
        record = model.get_by_id(table="record", field="zone_id", id_=d["id"])
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
            zone = model.get_by_id(table="zone", field="id", id_=zone_id)
        except Exception as e:
            return response(401, message=str(e))
        else:
            data = get_datum(zone)
            return response(200, data=data)


class GetDomainDataByProjectId(Resource):
    @auth.auth_required
    def get(self, project_id):

        try:
            user = model.get_by_id(
                table="user", field="project_id", id_=f"'{project_id}'"
            )
            user_id = user[0]["id"]
            zone = model.get_by_id(table="zone", field="user_id", id_=user_id)
        except Exception as e:
            return response(401, message=str(e))
        else:
            data = get_datum(zone)
            return response(200, data=data)


class DeleteDomain(Resource):
    @auth.auth_required
    def delete(self, zone_id):
        try:
            # other data (e.g record) deleted automatically
            # by cockroach when no PK existed
            model.delete(table="zone", field="id", value=zone_id)

            return response(200, message="Domain Deleted")
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
        if not model.is_unique(table="zone", field="zone", value=f"'{zone}'"):
            return response(401, message="Duplicate zone Detected")
        if validation.zone_validation(zone):
            return response(401, message="Named Error")

        # FIXME ValueError: invalid literal for int() with base 10: 'None' kafka
        try:
            zone_id = insert_zone(zone, project_id)
        except Exception as e:
            return response(401, message=str(e))
        else:
            # add zone config
            config_command = command.config_zone(zone, zone_id)
            producer.send(config_command)

            soa_record_id = insert_soa_default(zone_id)
            command.soa_default_command(soa_record_id)

            ns_record_id = insert_ns_default(zone_id)
            command.ns_default_command(ns_record_id)

            record_id = insert_cname(zone_id, zone)
            json_command = command.record_insert(record_id)
            producer.send(json_command)

            # just for feedback return value
            zone_data = {"zone": zone, "project_id": project_id}
            return response(200, data=zone_data, message="Inserted")


class ViewCommand(Resource):
    @auth.auth_required
    def get(self, zone_id):
        zone_data = model.read_by_id("zone", zone_id)["value"]
        command_data = command.config_zone(zone_data, zone_id)
        try:
            test = producer.send(command_data)
        except Exception as e:
            return response(401, message=str(e))
        else:
            data = {"send_status": test, "command": command_data}
            return response(200, data=data, message=test)
