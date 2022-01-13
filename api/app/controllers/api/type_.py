from flask import Response
from flask_restful import Resource, reqparse

from app.helpers.rest import response
from app.middlewares import auth
from app.models import type_ as db


class GetTypeData(Resource):
    @auth.auth_required
    def get(self) -> Response:
        try:
            types = db.get_all()
            if not types:
                return response(404, message="type not found")

            return response(200, data=types)
        except Exception:
            return response(500)


class GetTypeDataId(Resource):
    @auth.auth_required
    def get(self, type_id: int) -> Response:
        try:
            type_ = db.get(type_id)
            if not type_:
                return response(404, message="type not found")

            return response(200, data=type_)
        except Exception:
            return response(500)


class TypeAdd(Resource):
    @auth.auth_required
    def post(self) -> Response:
        parser = reqparse.RequestParser()
        parser.add_argument("type", type=str, required=True)
        args = parser.parse_args()
        type_ = args["type"]

        if not type_:
            return response(422)

        try:
            type_ = db.add(type_)
            return response(201, data=type_)
        except Exception:
            return response(500)


class TypeEdit(Resource):
    @auth.auth_required
    def put(self, type_id: int) -> Response:
        parser = reqparse.RequestParser()
        parser.add_argument("type", type=str, required=True)
        args = parser.parse_args()
        type_ = args["type"]

        if not type_:
            return response(422)

        try:
            _type = db.get(type_id)
            if not _type:
                return response(404, message="type not found")

            type_ = db.update(type_, type_id)
            return response(200, data=type_)
        except Exception:
            return response(500)


class TypeDelete(Resource):
    @auth.auth_required
    def delete(self, type_id: int) -> Response:
        try:
            _type = db.get(type_id)
            if not _type:
                return response(404, message="type not found")

            db.delete(type_id)
            return response(204)
        except Exception:
            return response(500)
