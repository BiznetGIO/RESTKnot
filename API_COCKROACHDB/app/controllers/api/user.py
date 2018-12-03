from flask_restful import Resource, reqparse, fields
from app.helpers.rest import *
from app.helpers.memcache import *
from app.middlewares.auth import jwt_required
import datetime
from app.models import model as db


class UserdataResource(Resource):
    @jwt_required
    def get(self):
        obj_userdata = list()
        
        try:
            results = db.get_all("userdata")
        except Exception:
            return response(200, message="Users Data Not Found")
        else:
            for i in results :
                data = {
                    "userdata_id": str(i['userdata_id']),
                    "email" : i['email'],
                    "first_name" : i['first_name'],
                    "last_name" : i['last_name'],
                    "location" : i['location'],
                    "city" : i['city'],
                    "province" : i['province'],
                    "created_at": str(i['created_at'])
                }
                obj_userdata.append(data)
            return response(200, data=obj_userdata)


class UserdataResourceById(Resource):
    @jwt_required
    def get(self, userdata_id):
        obj_userdata = []
        results = db.get_by_id(
                    table="userdata",
                    field="userdata_id",
                    value=userdata_id
                )

        for i in results :
            data = {
                "userdata_id": str(i['userdata_id']),
                "email" : i['email'],
                "first_name" : i['first_name'],
                "last_name" : i['last_name'],
                "location" : i['location'],
                "city" : i['city'],
                "province" : i['province'],
                "created_at": str(i['created_at'])
            }
            obj_userdata.append(data)
        return response(200, data=obj_userdata)


class UserdataInsert(Resource):
    # @jwt_required
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('email', type=str, required=True)
        parser.add_argument('first_name', type=str, required=True)
        parser.add_argument('last_name', type=str, required=True)
        parser.add_argument('location', type=str, required=True)
        parser.add_argument('city', type=str, required=True)
        parser.add_argument('province', type=str, required=True)
        args = parser.parse_args()

        data_insert = {
            "email" : args['email'],
            "first_name" : args['first_name'],
            "last_name" : args['last_name'],
            "location" : args['location'],
            "city" : args['city'],
            "province" : args['province']
        }
        try:
            result = db.insert(table="userdata", data=data_insert)
        except Exception as e:
            message = {
                "status": False,
                "error": str(e)
            }
        else:
            message = {
                "status": True,
                "data": data_insert,
                "id": result
            }
        finally:
            return response(200, message=message,)


class UserdataRemove(Resource):
    @jwt_required
    def delete(self, userdata_id):
        try:
            db.delete(
                    table="userdata", 
                    field='userdata_id',
                    value=userdata_id
                )
        except Exception as e:
            message = {
                "status": False,
                "error": str(e)
            }
        else:
            message = "removing"

        finally:
            return response(200, message=message)


class UserdataUpdate(Resource):
    @jwt_required
    def put(self, userdata_id):
        parser = reqparse.RequestParser()
        parser.add_argument('email', type=str, required=True)
        parser.add_argument('first_name', type=str, required=True)
        parser.add_argument('last_name', type=str, required=True)
        parser.add_argument('location', type=str, required=True)
        parser.add_argument('city', type=str, required=True)
        parser.add_argument('province', type=str, required=True)
        args = parser.parse_args()

        data = {
            "where":{
                "userdata_id": userdata_id
            },
            "data":{
                "email" : args['email'],
                "first_name" : args['first_name'],
                "last_name" : args['last_name'],
                "location" : args['location'],
                "city" : args['city'],
                "province" : args['province']
            }
        }

        
        try:
            db.update("userdata", data=data)
        except Exception as e:
            message = {
                "status": False,
                "error": str(e)
            }
        else:
            message = {
                "status": True,
                "data": data
            }
        finally:
            return response(200, message=message)

