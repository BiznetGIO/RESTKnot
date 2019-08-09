from flask_restful import Resource, reqparse
from app.helpers.rest import response
from app.models import model
from app.libs import utils
from app.middlewares import auth


class GetSerialData(Resource):
    @auth.auth_required
    def get(self):
        result = list()
        try:
            data_serial = model.read_all("serial")
        except Exception as e:
            return response(401, message=str(e))
        else:
            for i in data_serial:
                record = model.read_by_id("record", i["record"])
                types = model.read_by_id("type", record['type'])
                ttl = model.read_by_id("ttl", record['ttl'])
                zone = model.read_by_id("zone", record['zone'])
                data = {
                    "key": i['key'],
                    "name": i['name'],
                    "value": i['value'],
                    "record": record,
                    "ttl": ttl,
                    "type": types,
                    "zone": zone
                }
                result.append(data)
            return response(200, data=result)


class GetSerialDataId(Resource):
    @auth.auth_required
    def get(self, key):
        try:
            data_serial = model.read_by_id("serial", key)
        except Exception as e:
            return response(401, message=str(e))
        else:
            record = model.read_by_id("record", data_serial["record"])
            types = model.read_by_id("type", record['type'])
            ttl = model.read_by_id("ttl", record['ttl'])
            zone = model.read_by_id("zone", record['zone'])
            data = {
                "key": data_serial['key'],
                "name": data_serial['name'],
                "value": data_serial['value'],
                "record": record,
                "ttl": ttl,
                "type": types,
                "zone": zone
            }
            return response(200, data=data)


class SerialAdd(Resource):
    @auth.auth_required
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('value', type=str, required=True)
        parser.add_argument('name', type=str, required=True)
        parser.add_argument('id_record', type=str, required=True)
        args = parser.parse_args()
        serial = args["value"]
        name = args["name"]
        record_key = args["id_record"]
        key = utils.get_last_key("serial")

        # Check Relation
        if model.check_relation("record", record_key):
            return response(401, message="Relation to Record error Check Your Key")
        
        # Validation
        if not utils.check_record_serial(record_key):
            return response(401, message="No Serial Record")

        data = {
            "key": key,
            "value": serial,
            "name": name,
            "record": record_key,
            "created_at": utils.get_datetime()
        }
        try:
            model.insert_data("serial", key, data)
        except Exception as e:
            return response(401, message=str(e))
        else:
            return response(200, data=data, message="Inserted")


class SerialEdit(Resource):
    @auth.auth_required
    def put(self, key):
        parser = reqparse.RequestParser()
        parser.add_argument('value', type=str, required=True)
        parser.add_argument('name', type=str, required=True)
        parser.add_argument('id_record', type=str, required=True)
        args = parser.parse_args()
        serial = args["value"]
        name = args["name"]
        record_key = args["id_record"]
        
        # Check Relation
        if model.check_relation("record", record_key):
            return response(401, message="Relation to Record error Check Your Key")
            
        if not utils.check_record_serial(record_key):
            return response(401, message="No Serial Record")

        data = {
            "key": key,
            "value": serial,
            "name": name,
            "record": record_key,
            "created_at": utils.get_datetime()
        }
        try:
            model.update("serial", key, data)
        except Exception as e:
            return response(401, message=str(e))
        else:
            return response(200, data=data, message="Edited")
        

class SerialDelete(Resource):
    @auth.auth_required
    def delete(self, key):
        try:
            data = model.delete("serial", key)
        except Exception as e:
            return response(401, message=str(e))
        else:
            return response(200, data=data, message="Deleted")