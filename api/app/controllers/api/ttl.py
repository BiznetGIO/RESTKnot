from flask_restful import Resource, reqparse
from app.helpers.rest import response
from app.models import model
from app.models import ttl as ttl_model
from app.middlewares import auth


class GetTtlData(Resource):
    @auth.auth_required
    def get(self):
        try:
            ttls = model.get_all("ttl")
            if not ttls:
                return response(404)

            return response(200, data=ttls)
        except Exception as e:
            return response(500, message=str(e))


class GetTtlDataId(Resource):
    @auth.auth_required
    def get(self, ttl_id):
        try:
            ttl = model.get_one(table="ttl", field="id", value=ttl_id)
            if not ttl:
                return response(404)

            return response(200, data=ttl)
        except Exception as e:
            return response(500, message=str(e))


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

            return response(201, data=data_)
        except Exception as e:
            return response(500, message=str(e))


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
            return response(200, data=data.get("data"))
        except Exception as e:
            return response(500, message=str(e))


class TtlDelete(Resource):
    @auth.auth_required
    def delete(self, ttl_id):
        try:
            model.delete(table="ttl", field="id", value=ttl_id)
            return response(204)
        except Exception as e:
            return response(500, message=str(e))
