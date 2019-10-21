from flask_restful import Resource, reqparse
from app.helpers.rest import response
from app.models import model
from app.libs import utils
from app.middlewares import auth


class GetTtlData(Resource):
    @auth.auth_required
    def get(self):
        try:
            data = model.get_all("zn_ttl")
        except Exception as e:
            return response(401, message=str(e))
        else:
            return response(200, data=data)


class GetTtlDataId(Resource):
    @auth.auth_required
    def get(self, ttl_id):
        try:
            data = model.get_by_id(table="zn_ttl", field="id_ttl", user_id=ttl_id)
        except Exception as e:
            return response(401, message=str(e))
        else:
            return response(200, data=data)


class TtlAdd(Resource):
    @auth.auth_required
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("ttl", type=str, required=True)
        args = parser.parse_args()
        ttl = args["ttl"]
        key = utils.get_last_key("ttl")
        data = {"nm_ttl": ttl}
        try:
            model.insert("zn_ttl", data)
        except Exception as e:
            return response(401, message=str(e))
        else:
            return response(200, data=data, message="Inserted")


class TtlEdit(Resource):
    @auth.auth_required
    def put(self, ttl_id):
        parser = reqparse.RequestParser()
        parser.add_argument("ttl", type=str, required=True)
        args = parser.parse_args()
        ttl = args["ttl"]
        data = {"where": {"id_ttl": ttl_id}, "data": {"nm_ttl": ttl}}
        try:
            model.update("zn_ttl", data=data)
        except Exception as e:
            return response(401, message=str(e))
        else:
            return response(200, data=data, message="Edited")


class TtlDelete(Resource):
    @auth.auth_required
    def delete(self, ttl_id):
        try:
            data = model.delete(table="zn_ttl", field="id_ttl", value=ttl_id)
        except Exception as e:
            return response(401, message=str(e))
        else:
            return response(200, data=data, message="Deleted")
