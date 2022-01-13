from flask import Response
from flask_restful import Resource, reqparse

from app.helpers.rest import response
from app.middlewares import auth
from app.models import ttl as db


class GetTtlData(Resource):
    @auth.auth_required
    def get(self) -> Response:
        try:
            ttls = db.get_all()
            if not ttls:
                return response(404, message="ttl not found")

            return response(200, data=ttls)
        except Exception as e:
            return response(500, message=f"{e}")


class GetTtlDataId(Resource):
    @auth.auth_required
    def get(self, ttl_id: int) -> Response:
        try:
            ttl = db.get(ttl_id)
            if not ttl:
                return response(404, message="ttl not found")

            return response(200, data=ttl)
        except Exception as e:
            return response(500, message=f"{e}")


class TtlAdd(Resource):
    @auth.auth_required
    def post(self) -> Response:
        parser = reqparse.RequestParser()
        parser.add_argument("ttl", type=str, required=True)
        args = parser.parse_args()
        ttl = args["ttl"]

        if not ttl:
            return response(422)

        try:
            ttl = db.add(ttl)
            return response(201, data=ttl)
        except Exception as e:
            return response(500, message=f"{e}")


class TtlEdit(Resource):
    @auth.auth_required
    def put(self, ttl_id: int) -> Response:
        parser = reqparse.RequestParser()
        parser.add_argument("ttl", type=str, required=True)
        args = parser.parse_args()
        ttl = args["ttl"]

        if not ttl:
            return response(422)

        try:
            _ttl = db.get(ttl_id)
            if not _ttl:
                return response(404, message="ttl not found")

            ttl = db.update(ttl, ttl_id)
            return response(200, data=ttl)
        except Exception as e:
            return response(500, message=f"{e}")


class TtlDelete(Resource):
    @auth.auth_required
    def delete(self, ttl_id: int) -> Response:
        try:
            _ttl = db.get(ttl_id)
            if not _ttl:
                return response(404, message="ttl not found")

            db.delete(ttl_id)
            return response(204)
        except Exception as e:
            return response(500, message=f"{e}")
