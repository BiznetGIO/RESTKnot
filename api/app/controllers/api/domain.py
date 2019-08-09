from flask_restful import Resource, reqparse
from app.helpers.rest import response
from app.models import model
from app.libs import utils
from app.libs import validation
from app.helpers import command
from app.helpers import producer
from app.middlewares import auth
import os


def add_soa_record(zone_key, record_key):
    record_data = {
        "key": record_key,
        "value": "@",
        "zone": zone_key,
        "type": "4",
        "ttl": "6",
        "created_at": utils.get_datetime(),
        "serial": False
    }

    try:
        model.insert_data("record", record_key, record_data)
    except Exception as e:
        return response(401, message=str(e))

    date_data = utils.soa_time_set()+"01"
    default_soa_content = os.environ.get("DEFAULT_SOA_CONTENT", os.getenv("DEFAULT_SOA_CONTENT"))
    default_soa_serial = os.environ.get("DEFAULT_SOA_SERIAL", os.getenv("DEFAULT_SOA_SERIAL"))
    content_value = default_soa_content+" "+date_data+" "+default_soa_serial
    content_key = utils.get_last_key("content")
    content_data = {
        "key": content_key,
        "value": content_value,
        "record": record_key,
        "created_at": utils.get_datetime()
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
        "serial": False
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
            "created_at": utils.get_datetime()
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
        "serial": False
    }

    try:
        model.insert_data("record", record_key, record_data)
    except Exception as e:
        return response(401, message=str(e))


    content_key = utils.get_last_key("content")
    content_data = {
        "key": content_key,
        "value": zone_name+".",
        "record": record_key,
        "created_at": utils.get_datetime()
    }
    try:
        model.insert_data("content", content_key, content_data)
    except Exception as e:
        return response(401, message=str(e))

class GetDomainData(Resource):
    @auth.auth_required
    def get(self):
        results = list()
        try:
            data_zone = model.read_all("zone")
        except Exception as e:
            return response(401, message=str(e))
        
        for i in data_zone:
            user = model.read_by_id("user", i['user'])
            record = model.record_by_zone(i['key'])
            data = {
                "key": i['key'],
                "value": i['value'],
                "created_at": i['created_at'],
                "user": user,
                "record": record
            }
            results.append(data)
        return response(200, data=results)


class GetDomainDataByProjectId(Resource):
    @auth.auth_required
    def get(self, project_id):
        results = list()
        user = dict()
        try:
            data_user = model.read_all("user")
        except Exception as e:
            return response(401, message=str(e))
        else: 
            for i in data_user:
                if i['project_id'] == project_id:
                    user = i
                    break
        try:
            data_zone = model.read_all("zone")
        except Exception as e:
            return response(401, message=str(e))
        else:
            for i in data_zone:
                if i['user'] == user['key']:
                    user = model.read_by_id("user", i['user'])
                    record = model.record_by_zone(i['key'])
                    data = {
                        "key": i['key'],
                        "value": i['value'],
                        "created_at": i['created_at'],
                        "user": user,
                        "record": record
                    }
                    results.append(data)
            return response(200, data=results)


class GetDomainDataId(Resource):
    @auth.auth_required
    def get(self, key):
        try:
            data_zone = model.read_by_id("zone", key)
        except Exception as e:
            return response(401, message=str(e))
        else:
            user = model.read_by_id("user", data_zone['user'])
            record = model.record_by_zone(data_zone['key'])
            data = {
                "key": data_zone['key'],
                "value": data_zone['value'],
                "created_at": data_zone['created_at'],
                "user": user,
                "record": record
            }
            return response(200, data=data)


class DeleteDomain(Resource):
    @auth.auth_required
    def delete(self, key):
        try:
            record = model.record_by_zone(key)
        except Exception as e:
            return response(401, message="Record Not Found | "+str(e))
        else:
            for i in record:
                try:
                    model.record_delete(i['key'])
                except Exception as e:
                    print(e)
        try:
            model.delete("zone", key)
        except Exception as e:
            return response(401, message=str(e))
        else:
            return response(200, message="Domain Or Zone Deleted")


class AddDomain(Resource):
    @auth.auth_required
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('zone', type=str, required=True)
        parser.add_argument('project_id', type=str, required=True)
        args = parser.parse_args()
        zone = args['zone']
        project_id = args['project_id']
        user = model.get_user_by_project_id(project_id)['key']
        zone_key = utils.get_last_key("zone")
        
        # Validation Unique Zone
        if utils.check_unique("zone", "value", zone):
            return response(401, message="Duplicate zone Detected")
        # Validation Zone Name
        if validation.zone_validation(zone):
            return response(401, message="Named Error")
        # Check Relation Zone to User
        if model.check_relation("user", user):
            return response(401, message="Relation to user error Check Your Key")
        
       
        zone_data = {
            "key": zone_key,
            "value": zone,
            "created_at": utils.get_datetime(),
            "user": user,
        }
        try:
            model.insert_data("zone", zone_key, zone_data)
        except Exception as e:
            return response(401, message=str(e))
        else:

            # Adding Zone Config
            config_command = command.config_zone(zone, zone_key)
            producer.send(config_command)
            # ADDING DEFAULT RECORD   
            record_key_soa = utils.get_last_key("record")
            add_soa_record(zone_key, record_key_soa)
            command.soa_default_command(record_key_soa)

            record_key_ns = utils.get_last_key("record")
            add_ns_default(zone_key, record_key_ns)
            command.ns_default_command(record_key_ns)

            record_key_cname = utils.get_last_key("record")
            add_cname_default(zone_key, record_key_cname, zone)
            json_command = command.record_insert(record_key_cname)
            producer.send(json_command)
            # DEFAULT RECORD END

            return response(200, data=zone_data, message="Inserted")

        


class ViewCommand(Resource):
    @auth.auth_required
    def get(self, key):
        zone_data = model.read_by_id("zone", key)['value']
        command_data = command.config_zone(zone_data, key)
        try:
            test = producer.send(command_data)
        except Exception as e:
            return response(401, message=str(e))
        else:
            data ={
                "send_status": test,
                "command": command_data
            }
            return response(200, data=data, message=test)
            