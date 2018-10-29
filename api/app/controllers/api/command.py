from flask_restful import Resource, reqparse, request
from app.helpers.rest import *
from app.models import api_models as db
from app.helpers import cmd_parser as parse
from app.helpers import command as cmd
from app.libs import utils


class SendCommand(Resource):
    def get(self):
        pass
        # command = utils.get_command(request.path)
        # try:
        #     respons = db.result(command)
        # except Exception:
        #     respons = None
        # else:
        #     return response(200, data=respons)


    def post(self):
        json_req = request.get_json(force=True)
        command = utils.get_command(request.path)
        init_data = parse.parser(json_req, command)
        respons = dict()
        if init_data['action'] == 'conf-insert':
            tags = dict()
            for i in init_data['data']:
                tags = i['tags']
            respons = cmd.config_insert(tags)
        elif init_data['action'] == 'zone-read':
            tags = dict()
            for i in init_data['data']:
                tags = i['tags']
                respons = cmd.zone_read(tags)
        elif init_data['action'] == 'zone-soa-insert':
            for i in init_data['data']:
                tags = i['tags']
            respons = cmd.zone_soa_insert_default(tags)
        return response(200, data=respons)