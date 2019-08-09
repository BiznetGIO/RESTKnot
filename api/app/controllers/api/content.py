from flask_restful import Resource, reqparse
from app.helpers.rest import response
from app.models import model
from app.libs import utils
from app.libs import validation
from app.middlewares import auth

class GetContentData(Resource):
    @auth.auth_required
    def get(self):
        results = list()
        try:
            data_content = model.read_all("content")
            print(data_content)
        except Exception as e:
            return response(401, message=str(e))
        else:
            for i in data_content:
                record = model.read_by_id("record", i['record'])
                types = model.read_by_id("type", record['type'])
                ttl = model.read_by_id("ttl", record['ttl'])
                zone = model.read_by_id("zone", record['zone'])
                data = {
                    "key": i['key'],
                    "value": i['value'],
                    "created_at": i['created_at'],
                    "record": record,
                    "ttl": ttl,
                    "type": types,
                    "zone": zone
                }
                results.append(data)
            return response(200, data=results)


class GetContentDataId(Resource):
    @auth.auth_required
    def get(self, key):
        try:
            data_content = model.read_by_id("content", key)
        except Exception as e:
            return response(401, message=str(e))
        else:
            record = model.read_by_id("record", data_content['record'])
            types = model.read_by_id("type", record['type'])
            ttl = model.read_by_id("ttl", record['ttl'])
            zone = model.read_by_id("zone", record['zone'])
            data = {
                "key": data_content['key'],
                "value": data_content['value'],
                "created_at": data_content['created_at'],
                "record": record,
                "ttl": ttl,
                "type": types,
                "zone": zone
            }
            return response(200, data=data)


class ContentAdd(Resource):
    @auth.auth_required
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('content', type=str, required=True)
        parser.add_argument('id_record', type=str, required=True)
        args = parser.parse_args()
        content = args["content"]
        content = content.lower()
        record = args["id_record"]

        key = utils.get_last_key("content")
        
        # Check Relation
        if model.check_relation("record", record):
            return response(401, message="Relation to Record error Check Your Key")
        # Validation
        if validation.content_validation(record, content):
            return response(401, message="Named Error")
        if validation.count_character(content):
            return response(401, message="Count Character Error")

        data = {
            "key": key,
            "value": content,
            "record": record,
            "created_at": utils.get_datetime()
        }
        try:
            model.insert_data("content", key, data)
        except Exception as e:
            return response(401, message=str(e))
        else:
            return response(200, data=data, message="Inserted")


class ContentEdit(Resource):
    @auth.auth_required
    def put(self, key):
        parser = reqparse.RequestParser()
        parser.add_argument('content', type=str, required=True)
        parser.add_argument('id_record', type=str, required=True)
        args = parser.parse_args()
        content = args["content"]
        content = content.lower()
        record = args["id_record"]
        
        # Check Relation
        if model.check_relation("record", record):
            return response(401, message="Relation to Record error Check Your Key")
        
        # Validation
        if validation.content_validation(record, content):
            return response(401, message="Named Error")
        if validation.count_character(content):
            return response(401, message="Count Character Error")

        data = {
            "key": key,
            "value": content,
            "record": record,
            "created_at": utils.get_datetime()
        }
        try:
            model.update("content", key, data)
        except Exception as e:
            return response(401, message=str(e))
        else:
            return response(200, data=data, message="Edited")
        

class ContentDelete(Resource):
    @auth.auth_required
    def delete(self, key):
        try:
            data = model.delete("content", key)
        except Exception as e:
            return response(401, message=str(e))
        else:
            return response(200, data=data, message="Deleted")