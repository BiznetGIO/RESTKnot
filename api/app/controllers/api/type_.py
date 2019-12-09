from flask_restful import Resource, reqparse
from app.helpers.rest import response
from app.models import model
from app.models import type_ as type_model
from app.middlewares import auth


class GetTypeData(Resource):
    @auth.auth_required
    def get(self):
        try:
            data = model.get_all("type")
            return response(200, data=data)
        except Exception as e:
            return response(401, message=str(e))


class GetTypeDataId(Resource):
    @auth.auth_required
    def get(self, type_id):
        try:
            type_ = model.get_one(table="type", field="id", value=type_id)
            return response(200, data=type_)
        except Exception as e:
            return response(401, message=str(e))


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
            return response(200, data=data, message="Inserted")
        except Exception as e:
            return response(401, message=str(e))


class TypeEdit(Resource):
    @auth.auth_required
    def put(self, type_id):
        parser = reqparse.RequestParser()
        parser.add_argument("type", type=str, required=True)
        args = parser.parse_args()

        try:
            type_model.is_exists(type_id)
            data = {"where": {"id": type_id}, "data": {"type": args["type"]}}
            model.update("type", data=data)
            return response(200, data=data.get("data"), message="Edited")
        except Exception as e:
            return response(401, message=str(e))


class TypeDelete(Resource):
    @auth.auth_required
    def delete(self, type_id):
        try:
            type_model.is_exists(type_id)
            data = model.delete(table="type", field="id", value=type_id)
            return response(200, data=data, message="Deleted")
        except Exception as e:
            return response(401, message=str(e))
