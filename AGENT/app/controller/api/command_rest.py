from flask_restful import Resource, reqparse, request
from command import read_rest
import json

class CommandRest(Resource):
    def get(self):
        pass

    def post(self):
        json_req = request.get_json(force=True)
        print(json_req)
        try:
            exec_com = read_rest(json_req)
        except Exception as e:
            return str(e)
        else:
            return exec_com