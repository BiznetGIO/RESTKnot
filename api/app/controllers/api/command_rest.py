from flask_restful import Resource, reqparse, request
from app.helpers.rest import response
from app.models import model as db
from app.helpers import cmd_parser as parse
from app.helpers import command as cmd
from app.libs import utils
import json, os
from app.middlewares.auth import login_required
from app.helpers import cluster_task

class SendCommandRest(Resource):
    def get(self):
        pass

    @login_required
    def post(self):
        url_env = os.environ.get("SOCKET_AGENT_HOST", os.getenv('SOCKET_AGENT_HOST'))
        port = os.environ.get("SOCKET_AGENT_PORT", os.getenv('SOCKET_AGENT_PORT'))
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
                state = utils.change_state("id_zone", tags['id_zone'], "1")
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
                return response(401, message=str(e))
            else:
                http_respons = utils.send_http(url,respons)
                # state change
                if http_respons:
                    state = utils.change_state("id_record", id_record, "1")
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
            if http_response:
                state = utils.change_state("id_record", tags['id_record'], "1")
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
                return response(401, message=str(e) )
            else:
                for i in result:
                    state = None
                    http_response = utils.send_http(url,i['command'])
                    # state change
                    if http_response:
                        state = utils.change_state("id_record", i['id_record'], "1")
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
                return response(401, message=str(e))
            else:
                http_response = utils.send_http_cmd(url,respons)
                if http_response:
                    state = utils.change_state("id_record", tags['id_record'], "1")
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
                return response(401, data=result, message=str(e))
            else :
                http_response = utils.send_http_cmd(url,respons)
                # change state
                if http_response:
                    state = utils.change_state("id_record", tags['id_record'], "1")
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
            data_purge = cmd.conf_purge(tags)
            cmd.conf_begin_http(url)
            http_respons_purge = utils.send_http(url,data_purge)
            http_respons = utils.send_http(url,data)
            resp = {
                "zone-purge": http_respons_purge,
                "zone-unset": http_respons
            }
            cmd.conf_commit_http(url)
            return response(200, data=resp)
        
        if init_data['action'] == 'zone-unset':
            result = list()
            for i in init_data['data']:
                tags = i['tags']
            respons = list()
            try:
                res_begin = cmd.zone_begin_http(url,tags)
                respons.append(res_begin)
                json_command = cmd.zone_unset(tags)
                http_response = utils.send_http(url,json_command)
                respons.append(http_response)
                res_commit = cmd.zone_commit_http(url, tags)
                respons.append(res_commit)
            except Exception as e:
                return response(401, message=str(e))
            else:
                return response(200, data=respons)


        if init_data['action'] == 'cluster-master':
            result = list()
            for i in init_data['data']:
                tags = i['tags']
            
            try:
                master = cluster_task.cluster_task_master.delay(tags)
                result.append({
                    "id": str(master),
                    "state": master.state
                })
            except Exception as e:
                return response(401, message="Master Cluster Not Complete")
            else:
                return response(200, data=result, message="Master Cluster Processing")

        if init_data['action'] == 'cluster-slave':
            result = list()
            for i in init_data['data']:
                tags = i['tags']
            
            try:
                slave = cluster_task.cluster_task_slave.delay(tags)
                result.append({
                    "id": str(slave),
                    "state": slave.state
                })
            except Exception as e:
                return response(401, message="Slave Cluster Not Complete")
            else:
                return response(200, data=result, message="Slave Cluster Processing")

        if init_data['action'] == 'cluster-unset-master':
            result = []
            for i in init_data['data']:
                tags = i['tags']
            try:
                master_unset = cluster_task.unset_cluster_master.delay(tags)
                result.append({
                    "id": str(master_unset),
                    "state": master_unset.state
                })
            except Exception as e:
                return response(401, message=str(e))
            else:                
                return response(200, data=result)

        if init_data['action'] == 'cluster-unset-slave':
            result = []
            for i in init_data['data']:
                tags = i['tags']
            try:
                slave_unset = cluster_task.unset_cluster_slave.delay(tags)
                result.append({
                    "id": str(slave_unset),
                    "state": slave_unset.state
                })
            except Exception as e:
                return response(401, message=str(e))
            else:                
                return response(200, data=result)

        if init_data['action'] == 'conf-command':
            result = []
            exec_data = init_data['data'][0]['tags']
            try:
                cmd.conf_begin_http(url)
                http_res = utils.send_http(url, exec_data)
                cmd.conf_commit_http(url)
                result.append(http_res)
            except Exception as e:
                return response(401, message=str(e))
            else:                
                return response(200, data=exec_data)

        
        


