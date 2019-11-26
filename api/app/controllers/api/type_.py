from flask_restful import Resource, reqparse
from app.helpers.rest import response
from app.models import model
from app.libs import utils
from app.middlewares import auth


class GetTypeData(Resource):
    @auth.auth_required
    def get(self):
        try:
            data = model.get_all("type")
        except Exception as e:
            return response(401, message=str(e))
        else:
            return response(200, data=data)


class GetTypeDataId(Resource):
    @auth.auth_required
    def get(self, type_id):
        try:
            data = model.get_by_id(table="type", field="id", id_=type_id)
        except Exception as e:
            return response(401, message=str(e))
        else:
            return response(200, data=data)


class TypeAdd(Resource):
    @auth.auth_required
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("type", type=str, required=True)
        args = parser.parse_args()
        type_ = args["type"]

        data = {"type": type_}

        try:
            model.insert(table="type", data=data)
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

        data = {"where": {"id": type_id}, "data": {"type": args["type"]}}

        try:
            model.update("type", data=data)
        except Exception as e:
            return response(401, message=str(e))
        else:
            return response(200, data=data, message="Edited")


class TypeDelete(Resource):
    @auth.auth_required
    def delete(self, type_id):
        try:
            data = model.delete(table="type", field="id", value=type_id)
        except Exception as e:
            return response(401, message=str(e))
        else:
            return response(200, data=data, message="Deleted")
