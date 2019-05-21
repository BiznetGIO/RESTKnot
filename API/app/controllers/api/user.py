from flask_restful import Resource, reqparse, fields
from app.helpers.rest import *
from app.helpers.memcache import *
import datetime
from app.models import model as db
from app.middlewares.auth import login_required


class UserdataResource(Resource):
    @login_required
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
                    "user_id" : i['user_id'],
                    "project_id" : i['project_id'],
                    "created_at": str(i['created_at'])
                }
                obj_userdata.append(data)
            return response(200, data=obj_userdata)


class UserdataResourceById(Resource):
    @login_required
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
                    "user_id" : i['user_id'],
                    "project_id" : i['project_id'],
                    "created_at": str(i['created_at'])
                }
            obj_userdata.append(data)
        return response(200, data=obj_userdata)

class UserdataResourceByUserId(Resource):
    @login_required
    def get(self, user_id):
        obj_userdata = []
        results = db.get_by_id(
                    table="userdata",
                    field="user_id",
                    value=user_id
                )

        for i in results :
            data = {
                    "userdata_id": str(i['userdata_id']),
                    "user_id" : i['user_id'],
                    "project_id" : i['project_id'],
                    "created_at": str(i['created_at'])
                }
            obj_userdata.append(data)
        return response(200, data=obj_userdata)

class UserdataResourceByProjectId(Resource):
    @login_required
    def get(self,project_id):
        obj_userdata = list()
        try:
            results = db.get_all("userdata")
        except Exception :
            return response(200, "User Data Not Found")
        else :
            for i in results: 
                if i['project_id'] == str(project_id):
                    data = {
                        "userdata_id" : str(i['userdata_id']),
                        "user_id"     : i['user_id'],
                        "project_id"  : i["project_id"],
                        "created_at"  : str(i['created_at'])
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
            return response(200, message=message)

class UserdataRemove(Resource):
    @login_required
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
    @login_required
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

class UserDataZoneInsert(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id_zone', type=str, required=True)
        parser.add_argument("user-id", type=str, required=True, location='headers')
        args = parser.parse_args()
        
        args['user_id'] = args.pop('user-id')
        
        temp = db.get_all(table='userdata')
        
        for i in temp:
            if str(i['user_id']) == args['user_id']:
                userdata_id = str(i['userdata_id'])

        data_insert = {
            "id_zone" : args['id_zone'],
            "userdata_id"   : userdata_id
        }

       
        try :
            result = db.insert(table='zn_user_zone', data=data_insert)
        except Exception as e:
            message = {
                "status" : False,
                "error"  : str(e)
            }
        else:
            message = {
                "status" : True,
                "data"   : data_insert,
                "id"     : result
            }
        finally:
            return response(200, message=message)
        

class UserDataZoneResource(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument("user-id", type=str, required=True, location='headers')
        args = parser.parse_args()
        
        args['user_id'] = args.pop('user-id')

        temp = db.get_all(table='userdata')
        
        for i in temp:
            if str(i['user_id']) == args['user_id']:
                userdata_id = str(i['userdata_id'])
        


        obj_userdata = []
        results = db.get_by_id(
            table="zn_user_zone",
            field="userdata_id",
            value = userdata_id
        )
        for i in results : 
            data = {
                "id_user_zone" : str(i['id_user_zone']),
                "userdata_id"  : str(i['userdata_id']),
                "id_zone"      : str(i['id_zone'])
            }
            obj_userdata.append(data)
        return response(200, data = obj_userdata)