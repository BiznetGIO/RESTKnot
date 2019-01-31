from flask_restful import Resource, reqparse, request
from app.helpers.rest import *
from app.models import model as db
from app.helpers import cmd_parser as parse
from app.helpers import command as cmd
from app.libs import utils
# from app import sockets, BaseNamespace
import json, os
from app.middlewares.auth import login_required


class SendCommandRest(Resource):
    def get(self):
        pass

    @login_required
    def post(self):
        url_env = os.getenv("SOCKET_AGENT_HOST")
        port = os.getenv("SOCKET_AGENT_PORT")
        url_fix= url_env+":"+port
        url = url_fix+"/api/command_rest"
        json_req = request.get_json(force=True)
        command = utils.get_command(request.path)
        init_data = parse.parser(json_req, command)
        respons = dict()

        if init_data['action'] == 'conf-read':
            respons = cmd.conf_read()
            http_respons = utils.send_http(url, data=respons)
            return response(200, data=http_respons)

        if init_data['action'] == 'conf-insert':
            tags = dict()
            for i in init_data['data']:
                tags = i['tags']
            respons = cmd.config_insert(tags)
            cmd.conf_begin_http(url)
            http_respons = utils.send_http(url,respons)
            if http_respons:
                # state change
                state = utils.change_state("id_zone", tags['id_zone'], 1)
                db.update("zn_zone", data = state)

            cmd.conf_commit_http(url)
            return response(200, data=http_respons)

        if init_data['action'] == 'zone-read':
            tags = dict()
            for i in init_data['data']:
                tags = i['tags']
            respons = cmd.zone_read(tags)
            http_respons = utils.send_http(url, respons)
            return response(200, data=http_respons)

        if init_data['action'] == 'zone-soa-insert':
            result= list()
            for i in init_data['data']:
                tags = i['tags']
            begin_json = cmd.zone_begin(tags)
            begin_respon = utils.send_http(url,begin_json)
            result.append(begin_respon)

            try :
                id_record, respons = cmd.zone_soa_insert_default(tags)
            except Exception as e :
                respons = {
                    "Status" : False,
                    "Error" : str(e)
                }
                return response(400, message = respons)
            else:
                http_respons = utils.send_http(url,respons)
                # state change
                if http_respons:
                    state = utils.change_state("id_record", id_record, 1)
                    db.update("zn_record", data = state)

                result.append(http_respons)
                commit_json = cmd.zone_commit(tags)
                commit_response = utils.send_http(url,commit_json)
                result.append(commit_response)
                return response(200, data=result)

        if init_data['action'] == 'zone-begin':
            for i in init_data['data']:
                tags = i['tags']
            respons = cmd.zone_begin(tags)
            http_response = utils.send_http(url,respons)
            return response(200, data=http_response)

        if init_data['action'] == 'zone-commit':
            for i in init_data['data']:
                tags = i['tags']
            respons = cmd.zone_commit(tags)
            http_response = utils.send_http(url,respons)
            return response(200, data=http_response)

        if init_data['action'] == 'zone-insert':
            respons = list()
            for i in init_data['data']:
                tags = i['tags']
            json_begin = cmd.zone_begin_http(url,tags) 
            respons.append(json_begin)
            json_command = cmd.zone_insert(tags)
            http_response = utils.send_http(url,json_command)
            # change state
            if http_respons:
                state = utils.change_state("id_record", tags['id_record'], 1)
                try:
                    db.update("zn_record", data = state)
                except Exception as e:
                    print(e)
            respons.append(http_response)
            res_commit = cmd.zone_commit_http(url,tags)
            respons.append(res_commit)
            return response(200, data=respons)

        if init_data['action'] == 'zone-ns-insert':
            respons = list()
            for i in init_data['data']:
                tags = i['tags']
            res_begin = cmd.z_begin(url, tags)
            respons.append(res_begin)
            try :
                result = cmd.zone_ns_insert(tags)
            except Exception as e:
                respons = {
                    "Status" : False,
                    "Error" : str(e)
                }
                return response(400, message=respons )
            else:
                for i in result:
                    state = None
                    http_response = utils.send_http(url,i['command'])
                    # state change
                    if http_respons:
                        state = utils.change_state("id_record", i['id_record'], 1)
                        try:
                            db.update("zn_record", data = state)
                        except Exception as e:
                            print(e)
                    respons.append(http_response)

                res_commit = cmd.z_commit(url,tags)
                respons.append(res_commit)
                return response(200, data=respons)

        if init_data['action'] == 'zone-srv-insert':
            result = list()
            for i in init_data['data']:
                tags = i['tags']
            begin_json = cmd.zone_begin_http(url, tags)
            # begin_respon = utils.send_http(url,begin_json)
            result.append(begin_json)

            try:
                respons = cmd.zone_insert_srv(tags)
            except Exception as e:
                respons = {
                    "status" : False,
                    "error": str(e)
                }
                return response(400, data=result, message=respons)
            else:
                http_response = utils.send_http(url,respons)
                if http_respons:
                    state = utils.change_state("id_record", tags['id_record'], 1)
                    try:
                        db.update("zn_record", data = state)
                    except Exception as e:
                        print(e)

                result.append(http_response)
                commit_json = cmd.zone_commit_http(url, tags)
                # commit_response = utils.send_http(url,commit_json)
                result.append(commit_json)
                return response(200, data=result)

        if init_data['action'] == 'zone-mx-insert':
            result = list()
            for i in init_data['data']:
                tags = i['tags']

            begin_json = cmd.zone_begin_http(url, tags)
            # begin_respon = utils.send_http(url,begin_json)
            result.append(begin_json)

            try :
                respons = cmd.zone_insert_mx(tags)

            except Exception as e:
                respons = {
                    "status" : False,
                    "error": str(e)
                }
                return response(400, data=result, message=respons)
            else :
                http_response = utils.send_http(url,respons)
                # change state
                if http_respons:
                    state = utils.change_state("id_record", tags['id_record'], 1)
                    try:
                        db.update("zn_record", data = state)
                    except Exception as e:
                        print(e)

                result.append(http_response)
                commit_json = cmd.zone_commit_http(url, tags)
                result.append(commit_json)
                return response(200, data=result)

        # delete all zone
        if init_data['action'] == 'conf-unset':
            result = list()
            for i in init_data['data']:
                tags = i['tags']
            data = cmd.conf_unset(tags)
            cmd.conf_begin_http(url)
            http_respons = utils.send_http(url,data)
            cmd.conf_commit_http(url)
            return response(200, data=http_respons)
        
        if init_data['action'] == 'zone-unset':
            result = list()
            for i in init_data['data']:
                print(i)
                tags = i['tags']
            respons = list()
            res_begin = cmd.zone_begin_http(url,tags)
            respons.append(res_begin)
            json_command = cmd.zone_unset(tags)
            http_response = utils.send_http(url,json_command)
            respons.append(http_response)
            res_commit = cmd.zone_commit_http(url, tags)
            respons.append(res_commit)
            return response(200, data=respons)
