from flask_restful import Resource, reqparse
from app.helpers.rest import response
from app.models import model
from app.libs import utils
from app.libs import validation
from app.middlewares import auth

class GetZoneData(Resource):
    @auth.auth_required
    def get(self):
        results = list()
        try:
            data_zone = model.read_all("zone")
        except Exception as e:
            return response(401, message=str(e))
        
        for i in data_zone:
            user_data = model.read_by_id("user", i['user'])
            data = {
                "key": i['key'],
                "value": i['value'],
                "created_at": i['created_at'],
                "user": user_data
            }
            results.append(data)
        return response(200, data=results)


class GetZoneDataId(Resource):
    @auth.auth_required
    def get(self, key):
        try:
            data_zone = model.read_by_id("zone", key)
        except Exception as e:
            return response(401, message=str(e))
        else:
            user_data = model.read_by_id("user", data_zone['user'])
            data = {
                "key": data_zone['key'],
                "value": data_zone['value'],
                "created_at": data_zone['created_at'],
                "user": user_data
            }
            return response(200, data=data)


class ZoneAdd(Resource):
    @auth.auth_required
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('zone', type=str, required=True)
        parser.add_argument('id_user', type=str, required=True)
        args = parser.parse_args()
        zone = args["zone"]
        zone = zone.lower()
        id_user = args["id_user"]

        key = utils.get_last_key("zone")

        if utils.check_unique("zone", "value", zone):
            return response(401, message="Duplicate zone Detected")

        if validation.zone_validation(zone):
            return response(401, message="Named Error")
        
        data = {
            "key": key,
            "value": zone,
            "created_at": utils.get_datetime(),
            "user": id_user,
        }
        try:
            model.insert_data("zone", key, data)
        except Exception as e:
            return response(401, message=str(e))
        else:
            return response(200, data=data, message="Inserted")


class ZoneEdit(Resource):
    @auth.auth_required
    def put(self, key):
        parser = reqparse.RequestParser()
        parser.add_argument('zone', type=str, required=True)
        parser.add_argument('id_user', type=str, required=True)
        args = parser.parse_args()
        zone = args["zone"]
        zone = zone.lower()
        id_user = args["id_user"]
        if utils.check_unique("zone", "value", zone, key=key):
            return response(401, message="Duplicate zone Detected")
        if validation.zone_validation(zone):
            return response(401, message="Named Error")
        data = {
            "key": key,
            "value": zone,
            "created_at": utils.get_datetime(),
            "user": id_user,
        }
        try:
            model.update("zone", key, data)
        except Exception as e:
            return response(401, message=str(e))
        else:
            return response(200, data=data, message="Edited")
        

class ZoneDelete(Resource):
    @auth.auth_required
    def delete(self, key):
        try:
            data = model.delete("zone", key)
        except Exception as e:
            return response(401, message=str(e))
        else:
            return response(200, data=data, message="Deleted")