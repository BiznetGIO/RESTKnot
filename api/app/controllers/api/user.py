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
            return response(200, data=users)
        except Exception as e:
            return response(401, message=str(e))


class GetUserDataId(Resource):
    @auth.auth_required
    def get(self, user_id):
        try:
            user = model.get_one(table="user", field="id", value=user_id)
        except Exception as e:
            return response(401, message=str(e))
        else:
            return response(200, data=user)


class UserDelete(Resource):
    @auth.auth_required
    def delete(self, user_id):
        try:
            data = model.delete(table="user", field="id", value=user_id)
        except Exception as e:
            return response(401, message=str(e))
        else:
            return response(200, data=data, message="Deleted")


class UserSignUp(Resource):
    @auth.auth_required
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("email", type=str, required=True)
        args = parser.parse_args()
        email = args["email"]

        if not model.is_unique(table="user", field="email", value=f"{email}"):
            return response(401, message="Duplicate email Detected")

        data = {"email": email, "created_at": helpers.get_datetime()}
        try:
            validator.validate("EMAIL", email)
            model.insert(table="user", data=data)
        except Exception as e:
            return response(401, message=str(e))
        else:
            return response(200, data=data, message="Inserted")


class UserUpdate(Resource):
    @auth.auth_required
    def put(self, user_id):
        parser = reqparse.RequestParser()
        parser.add_argument("email", type=str, required=True)
        args = parser.parse_args()
        email = args["email"]
        args = parser.parse_args()

        if not model.is_unique(table="user", field="email", value=f"{email}"):
            return response(401, message="Duplicate email Detected")

        data = {"where": {"id": user_id}, "data": {"email": email}}
        try:
            validator.validate("EMAIL", email)
            model.update("user", data=data)
        except Exception as e:
            return response(401, message=str(e))
        else:
            return response(200, data=data.get("data"), message="Update Success")
