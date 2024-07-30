from flask import current_app, request
from flask_restful import Resource, reqparse

from app.helpers import helpers, validator
from app.middlewares import auth
from app.models import model
from app.vendors.rest import response


class GetUserData(Resource):
    @auth.auth_required
    def get(self):
        try:
            users = model.get_all("user")
            if not users:
                return response(404)

            return response(200, data=users)
        except Exception as e:
            current_app.logger.error(f"{e}")
            return response(500)


class GetUserDataId(Resource):
    @auth.auth_required
    def get(self):
        user_id = request.args.get("id")
        email = request.args.get("email")
        try:
            if not any((user_id, email)):
                return response(422, "Problems parsing parameters")

            if user_id:
                user = model.get_one(table="user", field="id", value=user_id)
            if email:
                user = model.get_one(table="user", field="email", value=email)
            if not user:
                return response(404)

            return response(200, data=user)
        except Exception as e:
            current_app.logger.error(f"{e}")
            return response(500)


class UserSignUp(Resource):
    @auth.auth_required
    def post(self):
        parser = reqparse.RequestParser()
        # import ipdb; ipdb.set_trace()
        parser.add_argument("email", type=str, required=True, location="form")
        args = parser.parse_args()
        # import ipdb; ipdb.set_trace()
        email = args["email"]
        # import ipdb; ipdb.set_trace()

        if not model.is_unique(table="user", field="email", value=f"{email}"):
            return response(409, message="Duplicate Email")

        try:
            validator.validate("EMAIL", email)
        except Exception as e:
            return response(422, message=f"{e}")

        try:
            data = {"email": email, "created_at": helpers.get_datetime()}

            inserted_id = model.insert(table="user", data=data)
            data_ = {"id": inserted_id, **data}
            return response(201, data=data_)
        except Exception as e:
            current_app.logger.error(f"{e}")
            return response(500)


class UserUpdate(Resource):
    @auth.auth_required
    def put(self, user_id):
        parser = reqparse.RequestParser()
        parser.add_argument("email", type=str, required=True, location="form")
        args = parser.parse_args()
        email = args["email"]
        args = parser.parse_args()

        if not model.is_unique(table="user", field="email", value=f"{email}"):
            return response(409, message="Duplicate Email")

        try:
            validator.validate("EMAIL", email)
        except Exception as e:
            return response(422, message=f"{e}")

        try:
            data = {"where": {"id": user_id}, "data": {"email": email}}
            row_count = model.update("user", data=data)
            if not row_count:
                return response(404)

            return response(200, data=data.get("data"))
        except Exception as e:
            current_app.logger.error(f"{e}")
            return response(500)


class UserDelete(Resource):
    @auth.auth_required
    def delete(self, user_id):
        try:
            row_count = model.delete(table="user", field="id", value=user_id)
            if not row_count:
                return response(404)

            return response(204)
        except Exception as e:
            current_app.logger.error(f"{e}")
            return response(500)
