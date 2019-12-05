from flask_restful import Resource, reqparse
from app.helpers.rest import response
from app.models import model
from app.models import user as user_model
from app.helpers import helpers
from app.middlewares import auth


class GetUserData(Resource):
    @auth.auth_required
    def get(self):
        try:
            data = model.get_all("user")
            user_data = user_model.get_datum(data)
            return response(200, data=user_data)
        except Exception as e:
            return response(401, message=str(e))


class GetUserDataId(Resource):
    @auth.auth_required
    def get(self, user_id):
        try:
            data = model.get_by_condition(table="user", field="id", value=user_id)
        except Exception as e:
            return response(401, message=str(e))
        else:
            user_data = user_model.get_datum(data)
            return response(200, data=user_data)


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
        parser.add_argument("project_id", type=str, required=True)
        args = parser.parse_args()
        project_id = args["project_id"]
        email = args["email"]

        if not model.is_unique(table="user", field="email", value=f"{email}"):
            return response(401, message="Duplicate email Detected")

        data = {
            "email": email,
            "project_id": project_id,
            "created_at": helpers.get_datetime(),
        }
        try:
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
        parser.add_argument("project_id", type=str, required=True)
        args = parser.parse_args()
        email = args["email"]
        args = parser.parse_args()

        if not model.is_unique(table="user", field="email", value=f"{email}"):
            return response(401, message="Duplicate email Detected")

        data = {
            "where": {"id": user_id},
            "data": {"project_id": args["project_id"], "email": email},
        }
        try:
            model.update("user", data=data)
        except Exception as e:
            return response(401, message=str(e))
        else:
            return response(200, data=data, message="Update Success")
