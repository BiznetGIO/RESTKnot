from flask_restful import Resource, reqparse, fields
from app.helpers.rest import *
from app.helpers.memcache import *
import datetime
from app.models import model as db


class UserdataResource(Resource):
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
                    "user_id" : i['first_name'],
                    "project_id" : i['last_name'],
                    "created_at": str(i['created_at'])
                }
                obj_userdata.append(data)
            return response(200, data=obj_userdata)


class UserdataResourceById(Resource):
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
                    "user_id" : i['first_name'],
                    "project_id" : i['last_name'],
                    "created_at": str(i['created_at'])
                }
            obj_userdata.append(data)
        return response(200, data=obj_userdata)


class UserdataInsert(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('project_id', type=str, required=True)
        parser.add_argument('user_id', type=str, required=True)
        args = parser.parse_args()

        data_insert = {
            "project_id" : args['project_id'],
            "user_id" : args['user_id'],
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
    def put(self, userdata_id):
        parser = reqparse.RequestParser()
        parser.add_argument('project_id', type=str, required=True)
        parser.add_argument('user_id', type=str, required=True)
        args = parser.parse_args()

        data = {
            "where":{
                "userdata_id": userdata_id
            },
            "data":{
                "project_id" : args['project_id'],
                "user_id" : args['user_id'],
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

