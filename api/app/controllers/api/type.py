from flask_restful import Resource, reqparse
from app.helpers.rest import response
from app.models import model
from app.libs import utils
from app.middlewares import auth


class GetTypeData(Resource):
    @auth.auth_required
    def get(self):
        try:
            data = model.read_all("type")
        except Exception as e:
            return response(401, message=str(e))
        else:
            return response(200, data=data)


class GetTypeDataId(Resource):
    @auth.auth_required
    def get(self, key):
        try:
            data = model.read_by_id("type", key)
        except Exception as e:
            return response(401, message=str(e))
        else:
            return response(200, data=data)


class TypeAdd(Resource):
    @auth.auth_required
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('type', type=str, required=True)
        parser.add_argument('serial', type=bool, required=True)
        args = parser.parse_args()
        types = args["type"]
        serial = args["serial"]
        key = utils.get_last_key("type")
        data = {
            "key": key,
            "value": types,
            "serial": serial
        }
        try:
            model.insert_data("type", key, data)
        except Exception as e:
            return response(401, message=str(e))
        else:
            return response(200, data=data, message="Inserted")


class TypeEdit(Resource):
    @auth.auth_required
    def put(self, key):
        parser = reqparse.RequestParser()
        parser.add_argument('type', type=str, required=True)
        parser.add_argument('serial', type=bool, required=True)
        args = parser.parse_args()
        types = args["type"]
        serial = args["serial"]
        data = {
            "key": key,
            "value": types,
            "serial": serial
        }
        try:
            model.update("type", key, data)
        except Exception as e:
            return response(401, message=str(e))
        else:
            return response(200, data=data, message="Edited")
        

class TypeDelete(Resource):
    @auth.auth_required
    def delete(self, key):
        try:
            data = model.delete("type", key)
        except Exception as e:
            return response(401, message=str(e))
        else:
            return response(200, data=data, message="Deleted")