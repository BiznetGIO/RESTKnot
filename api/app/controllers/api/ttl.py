from flask_restful import Resource, reqparse
from app.helpers.rest import response
from app.models import model
from app.libs import utils
from app.middlewares import auth


class GetTtlData(Resource):
    @auth.auth_required
    def get(self):
        try:
            data = model.read_all("ttl")
        except Exception as e:
            return response(401, message=str(e))
        else:
            return response(200, data=data)


class GetTtlDataId(Resource):
    @auth.auth_required
    def get(self, key):
        try:
            data = model.read_by_id("ttl", key)
        except Exception as e:
            return response(401, message=str(e))
        else:
            return response(200, data=data)


class TtlAdd(Resource):
    @auth.auth_required
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('ttl', type=str, required=True)
        args = parser.parse_args()
        ttl = args["ttl"]
        key = utils.get_last_key("ttl")
        data = {
            "key": key,
            "value": ttl
        }
        try:
            model.insert_data("ttl", key, data)
        except Exception as e:
            return response(401, message=str(e))
        else:
            return response(200, data=data, message="Inserted")


class TtlEdit(Resource):
    @auth.auth_required
    def put(self, key):
        parser = reqparse.RequestParser()
        parser.add_argument('ttl', type=str, required=True)
        args = parser.parse_args()
        ttl = args["ttl"]
        data = {
            "key": key,
            "value": ttl
        }
        try:
            model.update("ttl", key, data)
        except Exception as e:
            return response(401, message=str(e))
        else:
            return response(200, data=data, message="Edited")
        

class TtlDelete(Resource):
    @auth.auth_required
    def delete(self, key):
        try:
            data = model.delete("ttl", key)
        except Exception as e:
            return response(401, message=str(e))
        else:
            return response(200, data=data, message="Deleted")