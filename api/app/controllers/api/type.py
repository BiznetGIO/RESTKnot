from flask_restful import Resource, reqparse
from app.helpers.rest import response
from app.models import model
from app.libs import utils
from app.middlewares import auth


class GetTypeData(Resource):
    @auth.auth_required
    def get(self):
        try:
            data = model.get_all("zn_type")
        except Exception as e:
            return response(401, message=str(e))
        else:
            return response(200, data=data)


class GetTypeDataId(Resource):
    @auth.auth_required
    def get(self, type_id):
        try:
            data = model.get_by_id(table="zn_type", field="id_type", user_id=type_id)
        except Exception as e:
            return response(401, message=str(e))
        else:
            return response(200, data=data)


class TypeAdd(Resource):
    @auth.auth_required
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("type", type=str, required=True)
        parser.add_argument("serial", type=bool, required=True)
        args = parser.parse_args()
        types = args["type"]
        serial = args["serial"]
        key = utils.get_last_key("type")
        data = {"key": key, "value": types, "serial": serial}
        try:
            model.insert_data("type", key, data)
        except Exception as e:
            return response(401, message=str(e))
        else:
            return response(200, data=data, message="Inserted")


class TypeEdit(Resource):
    @auth.auth_required
    def put(self, type_id):
        parser = reqparse.RequestParser()
        parser.add_argument("type", type=str, required=True)
        args = parser.parse_args()

        data = {"where": {"id_type": type_id}, "data": {"nm_type": args["type"]}}
        try:
            model.update("zn_type", data=data)
        except Exception as e:
            return response(401, message=str(e))
        else:
            return response(200, data=data, message="Edited")


class TypeDelete(Resource):
    @auth.auth_required
    def delete(self, type_id):
        try:
            data = model.delete(table="zn_type", field="id_type", value=type_id)
        except Exception as e:
            return response(401, message=str(e))
        else:
            return response(200, data=data, message="Deleted")
