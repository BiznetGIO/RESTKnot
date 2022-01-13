from flask import Response, current_app, request
from flask_restful import Resource, reqparse

from app.helpers import validator
from app.helpers.rest import response
from app.middlewares import auth
from app.models import user as db


class GetUserData(Resource):
    @auth.auth_required
    def get(self) -> Response:
        try:
            users = db.get_all()
            if not users:
                return response(404)

            return response(200, data=users)
        except Exception as e:
            current_app.logger.error(f"{e}")
            return response(500)


class GetUserDataId(Resource):
    @auth.auth_required
    def get(self) -> Response:
        user_id = request.args.get("id")
        email = request.args.get("email")
        try:
            if not any((user_id, email)):
                return response(422, "problems parsing parameters")

            if user_id:
                user = db.get(int(user_id))
            if email:
                user = db.get_by_email(email)
            if not user:
                return response(404)

            return response(200, data=user)
        except Exception as e:
            current_app.logger.error(f"{e}")
            return response(500)


class UserSignUp(Resource):
    @auth.auth_required
    def post(self) -> Response:
        parser = reqparse.RequestParser()
        parser.add_argument("email", type=str, required=True)
        args = parser.parse_args()
        email = args["email"]

        try:
            validator.validate("EMAIL", email)
        except Exception as e:
            return response(422, message=f"{e}")

        try:
            _user = db.get_by_email(email)
            if _user:
                return response(409, message="user already exists")

            user = db.add(email)
            return response(201, data=user)
        except Exception as e:
            current_app.logger.error(f"{e}")
            return response(500)


class UserUpdate(Resource):
    @auth.auth_required
    def put(self, user_id: int) -> Response:
        parser = reqparse.RequestParser()
        parser.add_argument("email", type=str, required=True)
        args = parser.parse_args()
        email = args["email"]
        args = parser.parse_args()

        try:
            validator.validate("EMAIL", email)
        except Exception as e:
            return response(422, message=f"{e}")

        try:
            _user = db.get_by_email(email)
            if _user:
                return response(409, message="user already exists")

            user = db.update(email, user_id)
            return response(200, data=user)
        except Exception as e:
            current_app.logger.error(f"{e}")
            return response(500)


class UserDelete(Resource):
    @auth.auth_required
    def delete(self, user_id: int) -> Response:
        try:
            _user = db.get(user_id)
            if not _user:
                return response(404, message="user not found")

            db.delete(user_id)
            return response(204)
        except Exception as e:
            current_app.logger.error(f"{e}")
            return response(500)
