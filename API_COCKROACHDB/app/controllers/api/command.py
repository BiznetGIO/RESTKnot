from flask_restful import Resource, reqparse, request
from app.helpers.rest import *
from app.models import model as db
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
        
        if init_data['action'] == 'conf-read':
            respons = cmd.conf_read()
            # http_respons = utils.send_http("http://127.0.0.1:6967/api/command_rest", data=respons)
            # print(http_respons)
            socket_respons = utils.sendSocket(respons)
            return response(200, data=socket_respons)

        if init_data['action'] == 'conf-insert':
            tags = dict()
            for i in init_data['data']:
                tags = i['tags']
            respons = cmd.config_insert(tags)
            cmd.conf_begin()
            socket_respons = utils.sendSocket(respons)
            cmd.conf_commit()
            return response(200, data=socket_respons)
            # return response(200, data=respons)

        if init_data['action'] == 'zone-read':
            tags = dict()
            for i in init_data['data']:
                tags = i['tags']
            respons = cmd.zone_read(tags)
            # http_respons = utils.send_http("http://127.0.0.1:6967/api/command_rest", data=respons)
            socket_respons = utils.sendSocket(respons)
            return response(200, data=socket_respons)

        if init_data['action'] == 'zone-soa-insert':
            result= list()
            for i in init_data['data']:
                tags = i['tags']

            begin_json = cmd.zone_begin(tags)
            begin_respon = utils.sendSocket(begin_json)
            result.append(begin_respon)

            respons = cmd.zone_soa_insert_default(tags)
            socket_respons = utils.sendSocket(respons)
            result.append(socket_respons)

            commit_json = cmd.zone_commit(tags)
            commit_response = utils.sendSocket(commit_json)
            result.append(commit_response)
            
            return response(200, data=result)

        if init_data['action'] == 'zone-begin':
            for i in init_data['data']:
                tags = i['tags']
            respons = cmd.zone_begin(tags)
            socket_respons = utils.sendSocket(respons)
            return response(200, data=socket_respons)

        if init_data['action'] == 'zone-commit':
            for i in init_data['data']:
                tags = i['tags']
            respons = cmd.zone_commit(tags)
            socket_respons = utils.sendSocket(respons)
            return response(200, data=socket_respons)

        if init_data['action'] == 'zone-insert':
            respons = list()
            for i in init_data['data']:
                tags = i['tags']

            res_begin = cmd.z_begin(tags)
            respons.append(res_begin)
           
            json_command = cmd.zone_insert(tags)
            socket_respons = utils.sendSocket(json_command)
            print(socket_respons)
            respons.append(socket_respons)
            
            res_commit = cmd.z_commit(tags)
            respons.append(res_commit)
            return response(200, data=respons)

        if init_data['action'] == 'zone-ns-insert':
            respons = list()
            for i in init_data['data']:
                tags = i['tags']
            res_begin = cmd.z_begin(tags)
            respons.append(res_begin)
            resu = cmd.zone_ns_insert(tags)

            for i in resu:
                socket_respons = utils.sendSocket(i)
                respons.append(socket_respons)

            res_commit = cmd.z_commit(tags)
            respons.append(res_commit)
            return response(200, data=respons)

        if init_data['action'] == 'zone-srv-insert':
            result = list()
            for i in init_data['data']:
                tags = i['tags']

            begin_json = cmd.zone_begin(tags)
            begin_respon = utils.sendSocket(begin_json)
            result.append(begin_respon)

            respons = cmd.zone_insert_srv(tags)
            socket_respons = utils.sendSocket(respons)
            result.append(socket_respons)

            commit_json = cmd.zone_commit(tags)
            commit_response = utils.sendSocket(commit_json)
            result.append(commit_response)

        if init_data['action'] == 'zone-mx-insert':
            result = list()
            for i in init_data['data']:
                tags = i['tags']

            begin_json = cmd.zone_begin(tags)
            begin_respon = utils.sendSocket(begin_json)
            result.append(begin_respon)

            respons = cmd.zone_insert_mx(tags)
            socket_respons = utils.sendSocket(respons)
            result.append(socket_respons)

            commit_json = cmd.zone_commit(tags)
            commit_response = utils.sendSocket(commit_json)
            result.append(commit_response)
            return response(200, data=result)

        