from flask_restful import Resource, reqparse, request
from app.helpers.rest import *
from app.models import api_models as db
from app.helpers import cmd_parser as parse
from app.helpers import command as cmd
from app.libs import utils
from app import sockets, BaseNamespace
import json


class CmdNamespace(BaseNamespace):
    def initialize(self):
        self.response = None

    def on_response(self, *args):
        list_data = list(args)
        respons_sockets = list()
        for i in list_data:
            if i['data']['data'] == 'null':
                if i['data']['Description'] == '[]':
                    data = {
                        "command": i['data']['Description'],
                        "error": True,
                        "messages": "Block Type Command Not Parsing"
                    }
                else:
                    data = {
                        "status": True,
                        "messages": "Block Type Command Execute"
                    }
            else:
                data = {
                    "status": i['data']['result'],
                    "command": i['data']['Description'],
                    "receive": json.loads(i['data']['data'])
                }
            respons_sockets.append(data)
        self.response = respons_sockets

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
        
        # cmd_socket = sockets.define(namespace.CommandNameSpace, '/command')
        
        if init_data['action'] == 'conf-read':
            respons = cmd.conf_read()

        if init_data['action'] == 'conf-insert':
            tags = dict()
            for i in init_data['data']:
                tags = i['tags']
            respons = cmd.config_insert(tags)

        if init_data['action'] == 'zone-read':
            tags = dict()
            for i in init_data['data']:
                tags = i['tags']
            
            respons = cmd.zone_read(tags)


        if init_data['action'] == 'zone-soa-insert':
            for i in init_data['data']:
                tags = i['tags']
            respons = cmd.zone_soa_insert_default(tags)

        if init_data['action'] == 'zone-begin':
            for i in init_data['data']:
                tags = i['tags']
            respons = cmd.zone_begin(tags)

        if init_data['action'] == 'zone-commit':
            for i in init_data['data']:
                tags = i['tags']
            respons = cmd.zone_commit(tags)

        

        try:
            command = sockets.define(CmdNamespace, '/command')
            command.emit('command',respons)
            sockets.wait(seconds=1)
            socket_respons = command.response
        except Exception as e:
            print(e)
        return response(200, data=socket_respons)