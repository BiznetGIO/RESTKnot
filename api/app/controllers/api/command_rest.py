from flask_restful import Resource, reqparse, request
from app.helpers.rest import response
from app.models import model as db
from app.helpers import cmd_parser as parse
from app.helpers import command as cmd
from app.libs import utils
import json, os
from app.middlewares.auth import login_required
from app.helpers import cluster_task
from app.helpers import refresh_zone

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
            data = list()
            data.append(cmd.conf_begin_http_cl())
            respons = cmd.config_insert(tags)
            data.append(respons)
            data.append(cmd.conf_commit_http_cl())
            http_respons = utils.send_http(url, data)
            if http_respons:
                # state change
                state = utils.change_state("id_zone", tags['id_zone'], "1")
                db.update("zn_zone", data = state)            
            return response(200, data=http_respons)

        if init_data['action'] == 'zone-read':
            tags = dict()
            for i in init_data['data']:
                tags = i['tags']
            respons = cmd.zone_read(tags)
            http_respons = utils.send_http(url, respons)
            result = {
                "result": http_respons['data']['result'],
                "description": http_respons['data']['description'],
                "data": json.loads(http_respons['data']['data']),
            }
            print(result)
            return response(200, data=result)

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
            try:
                record = db.get_by_id("zn_zone", "id_zone", tags['id_zone'])[0]
            except Exception as e:
                return response(401, message=str(e))
            else:
                json_command = cmd.zone_begin(record['nm_zone'])
                http_response = utils.send_http(url, json_command)
                return response(200, data=http_response)

        if init_data['action'] == 'zone-commit':
            for i in init_data['data']:
                tags = i['tags']
            try:
                record = db.get_by_id("zn_zone", "id_zone", tags['id_zone'])[0]
            except Exception as e:
                return response(401, message=str(e))
            else:
                json_command = cmd.zone_commit(record['nm_zone'])
                http_response = utils.send_http(url, json_command)
                return response(200, data=http_response)

        if init_data['action'] == 'zone-insert':
            respons = list()
            for i in init_data['data']:
                tags = i['tags']
            record = db.get_by_id("v_record", "id_record", tags['id_record'])[0]    
            data = list()
            data.append(cmd.zone_begin(record['nm_zone']))
            json_command = cmd.zone_insert(tags)
            data.append(json_command)
            data.append(cmd.zone_commit(record['nm_zone']))
            respons = utils.send_http(url,data)
            if respons:
                state = utils.change_state("id_record", tags['id_record'], "1")
                try:
                    db.update("zn_record", data = state)
                except Exception as e:
                    print(e)
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
            data_send = list()

            data_send.append(cmd.conf_begin_http_cl())
            data = cmd.conf_unset(tags)
            data_purge = cmd.conf_purge(tags)
            data_send.append(data)
            data_send.append(data_purge)            
            data_send.append(cmd.conf_commit_http_cl())
            http_respons = utils.send_http(url,data_send)
            return response(200, data=http_respons)
        
        if init_data['action'] == 'zone-unset':
            result = list()
            for i in init_data['data']:
                tags = i['tags']
            respons = list()
            try:
                record = db.get_by_id("v_record", "id_record", tags['id_record'])[0]
            except Exception as e:
                return response(401, message=str(e))
            else:
                respons.append(cmd.zone_begin(record['nm_zone']))
                json_command = cmd.zone_unset(tags)
                respons.append(json_command)
                respons.append(cmd.zone_commit(record['nm_zone']))
                http_response = utils.send_http(url, respons)
                return response(200, data=http_response)


        if init_data['action'] == 'cluster-master':
            result = list()
            for i in init_data['data']:
                tags = i['tags']
            
            try:
                master = cluster_task.cluster_task_master.delay(tags)
            except Exception as e:
                return response(401, message="Master Cluster Not Complete")
            else:
                result.append({
                    "id": str(master),
                    "state": master.state
                })
                return response(200, data=result, message="Master Cluster Processing")

        if init_data['action'] == 'cluster-slave':
            result = list()
            for i in init_data['data']:
                tags = i['tags']
            
            try:
                slave = cluster_task.cluster_task_slave.delay(tags)
            except Exception as e:
                return response(401, message="Slave Cluster Not Complete")
            else:
                result.append({
                    "id": str(slave),
                    "state": slave.state
                })
                return response(200, data=result, message="Slave Cluster Processing")

        if init_data['action'] == 'cluster-unset-master':
            result = []
            for i in init_data['data']:
                tags = i['tags']
            try:
                master_unset = cluster_task.unset_cluster_master.delay(tags) 
            except Exception as e:
                return response(401, message=str(e))
            else:
                result.append({
                    "id": str(master_unset),
                    "state": master_unset.state
                })                
                return response(200, data=result)

        if init_data['action'] == 'cluster-unset-slave':
            result = []
            for i in init_data['data']:
                tags = i['tags']
            try:
                slave_unset = cluster_task.unset_cluster_slave.delay(tags)
                
            except Exception as e:
                return response(401, message=str(e))
            else:  
                result.append({
                    "id": str(slave_unset),
                    "state": slave_unset.state
                })              
                return response(200, data=result)

        if init_data['action'] == 'refresh-master':
            result = list()
            for i in init_data['data']:
                tags = i['tags']
            
            try:
                master = refresh_zone.refresh_zone_master.delay(tags['id_master'])
            except Exception as e:
                return response(401, message="Master Refresh Not Complete")
            else:
                result.append({
                    "id": str(master),
                    "state": master.state
                })
                return response(200, data=result, message="Master Refresh Processing")

        if init_data['action'] == 'refresh-slave':
            result = list()
            for i in init_data['data']:
                tags = i['tags']
            
            try:
                slave = refresh_zone.refresh_zone_slave.delay(tags)
            except Exception as e:
                return response(401, message="Slave Refresh Not Complete")
            else:
                result.append({
                    "id": str(slave),
                    "state": slave.state
                })
                return response(200, data=result, message="Slave Refresh Processing")

        
        


