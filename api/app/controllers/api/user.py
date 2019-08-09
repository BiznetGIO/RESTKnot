from flask_restful import Resource, reqparse
from app.helpers.rest import response
from app.models import model
from app.libs import utils
from app.middlewares import auth


class GetUserData(Resource):
    @auth.auth_required
    def get(self):
        try:
            data = model.read_all("user")
        except Exception as e:
            return response(401, message=str(e))
        else:
            return response(200, data=data)

class GetUserDataId(Resource):
    @auth.auth_required
    def get(self, key):
        try:
            data = model.read_by_id("user", key)
        except Exception as e:
            return response(401, message=str(e))
        else:
            return response(200, data=data)


class UserDelete(Resource):
    @auth.auth_required
    def delete(self, key):
        try:
            data = model.delete("user", key)
        except Exception as e:
            return response(401, message=str(e))
        else:
            return response(200, data=data, message="Deleted")
        

class UserSignUp(Resource):
    @auth.auth_required
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('email', type=str, required=True)
        parser.add_argument('project_id', type=str, required=True)
        args = parser.parse_args()
        project_id = args["project_id"]
        email = args["email"]
        
        key = utils.get_last_key("user")

        if utils.check_unique("user", "email", email):
            return response(401, message="Duplicate email Detected")
        
        data = {
            "key": key,
            "email": email,
            "project_id": project_id,
            "state": "inserted",
            "created_at": utils.get_datetime()
        }
        try:
            model.insert_data("/user", key, data)
        except Exception as e:
            return response(401, message=str(e))
        else:
            return response(200, data=data, message="Inserted")


class UserUpdate(Resource):
    @auth.auth_required
    def put(self, key):
        parser = reqparse.RequestParser()
        parser.add_argument('email', type=str, required=True)
        parser.add_argument('project_id', type=str, required=True)
        args = parser.parse_args()
        project_id = args["project_id"]
        email = args["email"]
        if utils.check_unique("user", "email", email, key=key):
            return response(401, message="Duplicate email Detected")
        data_update = {
            "key": key,
            "email": email,
            "project_id": project_id,
            "state": "edited",
            "created_at": utils.get_datetime()
        }
        
        try:
            model.update("user", key, data_update)
        except Exception as e:
            return response(401, message=str(e))
        else:
            return response(200, data=data_update, message="Update Success")