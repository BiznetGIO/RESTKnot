from flask_restful import Resource, reqparse
from app.helpers.rest import response
from app.models import model
from app.libs import utils
from app.middlewares import auth


def get_datum(data):
    if data is None:
        return

    results = []
    for d in data:
        datum = {
            "id": str(d["userdata_id"]),
            "email": d["email"],
            "project_id": d["project_id"],
            "created_at": str(d["created_at"]),
        }
        results.append(datum)
    return results


class GetUserData(Resource):
    @auth.auth_required
    def get(self):
        try:
            data = model.get_all("userdata")
            user_data = get_datum(data)
            return response(200, data=user_data)
        except Exception as e:
            return response(401, message=str(e))


class GetUserDataId(Resource):
    @auth.auth_required
    def get(self, userdata_id):
        try:
            data = model.get_by_id(
                table="userdata", field="userdata_id", user_id=userdata_id
            )
        except Exception as e:
            return response(401, message=str(e))
        else:
            user_data = get_datum(data)
            return response(200, data=user_data)


class UserDelete(Resource):
    @auth.auth_required
    def delete(self, userdata_id):
        try:
            data = model.delete(
                table="userdata", field="userdata_id", value=userdata_id
            )
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

        key = utils.get_last_key("userdata")

        if utils.check_unique("userdata", "email", email):
            return response(401, message="Duplicate email Detected")
        # FIXME "state" should be added
        data = {
            "email": email,
            "project_id": project_id,
            "created_at": utils.get_datetime(),
        }
        try:
            model.insert(table="userdata", data=data)
        except Exception as e:
            return response(401, message=str(e))
        else:
            return response(200, data=data, message="Inserted")


class UserUpdate(Resource):
    @auth.auth_required
    def put(self, userdata_id):
        parser = reqparse.RequestParser()
        parser.add_argument("email", type=str, required=True)
        parser.add_argument("project_id", type=str, required=True)
        args = parser.parse_args()
        email = args["email"]
        args = parser.parse_args()

        if utils.check_unique("userdata", "email", email):
            return response(401, message="Duplicate email Detected")
        data = {
            "where": {"userdata_id": userdata_id},
            "data": {"project_id": args["project_id"], "email": email},
        }
        try:
            model.update("userdata", data=data)
        except Exception as e:
            return response(401, message=str(e))
        else:
            return response(200, data=data, message="Update Success")
