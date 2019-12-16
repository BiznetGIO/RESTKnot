from flask_restful import Resource, reqparse
from app.helpers.rest import response
from app.models import model
from app.models import ttl as ttl_model
from app.middlewares import auth


class GetTtlData(Resource):
    @auth.auth_required
    def get(self):
        try:
            data = model.get_all("ttl")
            return response(200, data=data)
        except Exception as e:
            return response(401, message=str(e))


class GetTtlDataId(Resource):
    @auth.auth_required
    def get(self, ttl_id):
        try:
            ttl = model.get_one(table="ttl", field="id", value=ttl_id)
            return response(200, data=ttl)
        except Exception as e:
            return response(401, message=str(e))


class TtlAdd(Resource):
    @auth.auth_required
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("ttl", type=str, required=True)
        args = parser.parse_args()
        ttl = args["ttl"]

        data = {"ttl": ttl}
        try:
            inserted_id = model.insert(table="ttl", data=data)
            data_ = {"id": inserted_id, **data}

            return response(200, data=data_, message="Inserted")
        except Exception as e:
            return response(401, message=str(e))


class TtlEdit(Resource):
    @auth.auth_required
    def put(self, ttl_id):
        parser = reqparse.RequestParser()
        parser.add_argument("ttl", type=str, required=True)
        args = parser.parse_args()
        ttl = args["ttl"]

        try:
            ttl_model.is_exists(ttl_id)
            data = {"where": {"id": ttl_id}, "data": {"ttl": ttl}}
            model.update("ttl", data=data)
            return response(200, data=data.get("data"), message="Edited")
        except Exception as e:
            return response(401, message=str(e))


class TtlDelete(Resource):
    @auth.auth_required
    def delete(self, ttl_id):
        try:
            data = model.delete(table="ttl", field="id", value=ttl_id)
            return response(200, data=data, message="Deleted")
        except Exception as e:
            return response(401, message=str(e))
