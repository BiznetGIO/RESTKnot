from flask_restful import Resource, reqparse
from app.vendors.rest import response
from app.models import model
from app.middlewares import auth


class GetTypeData(Resource):
    @auth.auth_required
    def get(self):
        try:
            types = model.get_all("type")
            if not types:
                return response(404)

            return response(200, data=types)
        except Exception:
            return response(500)


class GetTypeDataId(Resource):
    @auth.auth_required
    def get(self, type_id):
        try:
            type_ = model.get_one(table="type", field="id", value=type_id)
            if not type_:
                return response(404)

            return response(200, data=type_)
        except Exception:
            return response(500)


class TypeAdd(Resource):
    @auth.auth_required
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("type", type=str, required=True)
        args = parser.parse_args()
        type_ = args["type"]

        data = {"type": type_}

        if not type_:
            return response(422)

        try:
            inserted_id = model.insert(table="type", data=data)

            data_ = {"id": inserted_id, **data}
            return response(201, data=data_)
        except Exception:
            return response(500)


class TypeEdit(Resource):
    @auth.auth_required
    def put(self, type_id):
        parser = reqparse.RequestParser()
        parser.add_argument("type", type=str, required=True)
        args = parser.parse_args()
        type_ = args["type"]

        if not type_:
            return response(422)

        try:
            data = {"where": {"id": type_id}, "data": {"type": type_}}
            row_count = model.update("type", data=data)
            if not row_count:
                return response(404)

            return response(200, data=data.get("data"))
        except Exception:
            return response(500)


class TypeDelete(Resource):
    @auth.auth_required
    def delete(self, type_id):
        try:
            row_count = model.delete(table="type", field="id", value=type_id)
            if not row_count:
                return response(404)

            return response(204)
        except Exception:
            return response(500)
