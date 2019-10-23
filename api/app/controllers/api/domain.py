from flask_restful import Resource, reqparse
from app.helpers.rest import response
from app.models import model
from app.libs import utils
from app.libs import validation
from app.helpers import command
from app.helpers import producer
from app.middlewares import auth
from app.controllers.api import user as user_api
import os


def add_soa_record(zone_key, record_key):
    record_data = {
        "key": record_key,
        "value": "@",
        "zone": zone_key,
        "type": "4",
        "ttl": "6",
        "created_at": utils.get_datetime(),
        "serial": False,
    }

    try:
        model.insert(table="record", data=record_data)
    except Exception as e:
        return response(401, message=str(e))

    date_data = utils.soa_time_set() + "01"
    default_soa_content = os.environ.get(
        "DEFAULT_SOA_CONTENT", os.getenv("DEFAULT_SOA_CONTENT")
    )
    default_soa_serial = os.environ.get(
        "DEFAULT_SOA_SERIAL", os.getenv("DEFAULT_SOA_SERIAL")
    )
    content_value = default_soa_content + " " + date_data + " " + default_soa_serial
    content_key = utils.get_last_key("content")
    content_data = {
        "key": content_key,
        "value": content_value,
        "record": record_key,
        "created_at": utils.get_datetime(),
    }
    try:
        model.insert_data("content", content_key, content_data)
    except Exception as e:
        return response(401, message=str(e))


def add_ns_default(zone_key, record_key):
    record_data = {
        "key": record_key,
        "value": "@",
        "zone": zone_key,
        "type": "5",
        "ttl": "6",
        "created_at": utils.get_datetime(),
        "serial": False,
    }

    try:
        model.insert_data("record", record_key, record_data)
    except Exception as e:
        return response(401, message=str(e))

    default_ns = os.environ.get("DEFAULT_NS", os.getenv("DEFAULT_NS"))
    default_ns = default_ns.split(" ")
    for i in default_ns:
        content_key = utils.get_last_key("content")
        content_data = {
            "key": content_key,
            "value": i,
            "record": record_key,
            "created_at": utils.get_datetime(),
        }
        try:
            model.insert_data("content", content_key, content_data)
        except Exception as e:
            return response(401, message=str(e))


def add_cname_default(zone_key, record_key, zone_name):
    record_data = {
        "key": record_key,
        "value": "www",
        "zone": zone_key,
        "type": "2",
        "ttl": "6",
        "created_at": utils.get_datetime(),
        "serial": False,
    }

    try:
        model.insert_data("record", record_key, record_data)
    except Exception as e:
        return response(401, message=str(e))

    content_key = utils.get_last_key("content")
    content_data = {
        "key": content_key,
        "value": zone_name + ".",
        "record": record_key,
        "created_at": utils.get_datetime(),
    }
    try:
        model.insert_data("content", content_key, content_data)
    except Exception as e:
        return response(401, message=str(e))


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
            record = model.get_by_id(table="record", field="zone_id", id_=zone_id)
            record_id = record[0]["id"]
        except Exception:
            return response(401, message="Record Not Found")
        else:
            model.delete(table="record", field="id", value=record_id)

        try:
            model.delete(table="zone", field="id", value=zone_id)
        except Exception as e:
            return response(401, message=str(e))
        else:
            return response(200, message="Domain and Zone Deleted")


class AddDomain(Resource):
    @auth.auth_required
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("zone", type=str, required=True)
        parser.add_argument("project_id", type=str, required=True)
        args = parser.parse_args()
        zone = args["zone"]
        project_id = args["project_id"]

        user = model.get_by_id(table="user", field="project_id", id_=f"'{project_id}'")
        user_id = user[0]["id"]

        # Validation Unique Zone
        if utils.check_unique("zone", "zone", zone):
            return response(401, message="Duplicate zone Detected")
        # Validation Zone Name
        if validation.zone_validation(zone):
            return response(401, message="Named Error")

        # Check Relation Zone to User
        # if model.check_relation("user", user_id):
        #     return response(401, message="Relation to user error Check Your Key")

        # FIXME ValueError: invalid literal for int() with base 10: 'None' kafka
        data = {"zone": zone, "user_id": user_id}
        try:
            zone_id = model.insert(table="zone", data=data)
            print(f"data: {data}")
        except Exception as e:
            return response(401, message=str(e))
        else:

            # Adding Zone Config
            config_command = command.config_zone(zone, zone_id)
            producer.send(config_command)

            # ADDING DEFAULT RECORD
            record_key_soa = utils.get_last_key("record")
            add_soa_record(zone_id, record_key_soa)
            command.soa_default_command(record_key_soa)

            record_key_ns = utils.get_last_key("record")
            add_ns_default(zone_id, record_key_ns)
            command.ns_default_command(record_key_ns)

            record_key_cname = utils.get_last_key("record")
            add_cname_default(zone_id, record_key_cname, zone)
            json_command = command.record_insert(record_key_cname)
            producer.send(json_command)
            # DEFAULT RECORD END

            return response(200, data=data, message="Inserted")


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
