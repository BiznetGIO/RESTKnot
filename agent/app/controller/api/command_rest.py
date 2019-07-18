from flask_restful import Resource, reqparse, request
from app.helpers.rest import response
from command import read_rest
from app.middlewares import check_on
import json


class CommandRest(Resource):
    def get(self):
        return 200
        
    def post(self):
        json_req = request.get_json(force=True)
        try:
            exec_com = read_rest(json_req)
        except Exception as e:
            return str(e)
        else:
            return exec_com

class CheckOnServer(Resource):
    def get(self):
        try:
            check_on.check_on_server()
            check_on.refreshZone()
        except Exception:
            return response(401, message="Error")
        else:
            return response(200, message="OK")
