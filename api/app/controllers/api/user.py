from flask_restful import Resource, reqparse
from app.helpers.rest import response
from app.models import model
from app.helpers import helpers
from app.middlewares import auth
from app.helpers import validator


class GetUserData(Resource):
    @auth.auth_required
    def get(self):
        try:
            users = model.get_all("user")
            if not users:
                return response(404)

            return response(200, data=users)
        except Exception:
            return response(500)


class GetUserDataId(Resource):
    @auth.auth_required
    def get(self, user_id):
        try:
            user = model.get_one(table="user", field="id", value=user_id)
            if not user:
                return response(404)

            return response(200, data=user)
        except Exception:
            return response(500)


class UserSignUp(Resource):
    @auth.auth_required
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("email", type=str, required=True)
        args = parser.parse_args()
        email = args["email"]

        if not model.is_unique(table="user", field="email", value=f"{email}"):
            return response(409, message="Duplicate Email")

        try:
            validator.validate("EMAIL", email)
        except Exception:
            return response(422)

        try:
            data = {"email": email, "created_at": helpers.get_datetime()}

            inserted_id = model.insert(table="user", data=data)
            data_ = {"id": inserted_id, **data}
            return response(201, data=data_)
        except Exception:
            return response(500)


class UserUpdate(Resource):
    @auth.auth_required
    def put(self, user_id):
        parser = reqparse.RequestParser()
        parser.add_argument("email", type=str, required=True)
        args = parser.parse_args()
        email = args["email"]
        args = parser.parse_args()

        if not model.is_unique(table="user", field="email", value=f"{email}"):
            return response(409, message="Duplicate Email")

        try:
            validator.validate("EMAIL", email)
        except Exception:
            return response(422)

        try:
            data = {"where": {"id": user_id}, "data": {"email": email}}
            row_count = model.update("user", data=data)
            if not row_count:
                return response(404)

            return response(200, data=data.get("data"))
        except Exception:
            return response(500)


class UserDelete(Resource):
    @auth.auth_required
    def delete(self, user_id):
        try:
            row_count = model.delete(table="user", field="id", value=user_id)
            if not row_count:
                return response(404)

            return response(204)
        except Exception:
            return response(500)
