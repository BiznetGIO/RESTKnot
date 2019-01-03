from flask_restful import Resource, reqparse, request
from app.helpers.rest import *
from app.models import api_models as db
from app.helpers import cmd_parser as cmd
from app.libs import utils


class ZoneName(Resource):
    def get(self):
        command = utils.get_command(request.path)
        try:
            respons = db.result(command)
        except Exception:
            respons = None
        else:
            return response(200, data=respons)


    def post(self):
        json_req = request.get_json(force=True)
        command = utils.get_command(request.path)
        init_data = cmd.parser(json_req, command)
        respons = dict()
        if init_data['action'] == 'insert':
            row = utils.check_row(init_data['data'])
            if row:
                respons = db.insert(init_data['data'])
                return response(200, data=respons)
            else:
                return response(200, message="Duplicate "+command)
        elif init_data['action'] == 'where':
            measurement = ""
            tags = dict()
            for i in init_data['data']:
                measurement = i['measurement']
                tags = i['tags']
            respons = db.row(measurement,tags)
        elif init_data['action'] == 'remove':
            measurement = ""
            tags = dict()
            for i in init_data['data']:
                measurement = i['measurement']
                tags = i['tags']
            respons = db.delete(measurement,tags)
        return response(200, data=respons)