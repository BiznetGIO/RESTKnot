from flask_restful import Resource, reqparse, request
from app.helpers.rest import response
from app.models import model as db
from app.helpers import cmd_parser as parse
from app.helpers import command as cmd
from app.libs import utils
# from app import sockets, BaseNamespace
import json, os
from app.middlewares.auth import login_required
from app.helpers import cl_command


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
            res_begin = cmd.zone_begin_http(url,tags)
            respons.append(res_begin)
            json_command = cmd.zone_unset(tags)
            http_response = utils.send_http(url,json_command)
            respons.append(http_response)
            res_commit = cmd.zone_commit_http(url, tags)
            respons.append(res_commit)
            return response(200, data=respons)

        if init_data['action'] == 'master-notify':
            result = list()
            for i in init_data['data']:
                tags = i['tags']
            respons = cmd.conf_set_notify_master(tags)
            for i in respons:
                server_port = i['cluster-set']['receive']['port']
                server_uri = "http://"+i['cluster-set']['receive']['uri']+":"+server_port+"/api/command_rest"
                cmd.conf_begin_http(server_uri)
                http_response = utils.send_http(server_uri,i)
                try:
                    for a in http_response['description']:
                        data_state = None
                        log_data = None
                        if a['cluster-set'] != "OK\n":
                            data_state = {
                                "where":{
                                    "id_notify_master" : str(i['cluster-set']['receive']['id_notify_master'])
                                },
                                "data":{
                                    "state" : "0"
                                }
                            }

                            log_data = {
                                "id_notify_master": str(i['cluster-set']['receive']['id_notify_master']),
                                "messages": a['cluster-set'],
                                "command_type": "add: "+i['cluster-set']['sendblock']['rtype']
                            }
                            # db.insert("cs_notify_master_log", log_data)
                            # db.update("cs_notify_master", data_state)
                        else:
                            data_state = {
                                "where":{
                                    "id_notify_master" : str(i['cluster-set']['receive']['id_notify_master'])
                                },
                                "data":{
                                    "state" : "1"
                                }
                            }
                            log_data = {
                                "id_notify_master": str(i['cluster-set']['receive']['id_notify_master']),
                                "messages": a['cluster-set'],
                                "command_type": "Add: "+i['cluster-set']['sendblock']['rtype']
                            }
                        db.insert("cs_notify_master_log", log_data)
                        db.update("cs_notify_master", data_state)
                except Exception:
                    pass
                cmd.conf_commit_http(server_uri)
                result.append(http_response)
            return response(200, data=result)

        if init_data['action'] == 'master-acl':
            result = list()
            for i in init_data['data']:
                tags = i['tags']
            respons = cmd.conf_set_acl_master(tags)
            for i in respons:
                server_port = i['cluster-set']['receive']['port']
                server_uri = "http://"+i['cluster-set']['receive']['uri']+":"+server_port+"/api/command_rest"
                cmd.conf_begin_http(server_uri)
                http_response = utils.send_http(server_uri,i)
                try:
                    for a in http_response['description']:
                        data_state = None
                        log_data = None
                        if a['cluster-set'] != "OK\n":
                            data_state = {
                                "where":{
                                    "id_acl_master" : str(i['cluster-set']['receive']['id_acl_master'])
                                },
                                "data":{
                                    "state" : "0"
                                }
                            }

                            log_data = {
                                "id_acl_master": str(i['cluster-set']['receive']['id_acl_master']),
                                "messages": a['cluster-set'],
                                "command_type": "Add: "+i['cluster-set']['sendblock']['rtype']
                            }
                        else:
                            data_state = {
                                "where":{
                                    "id_acl_master" : str(i['cluster-set']['receive']['id_acl_master'])
                                },
                                "data":{
                                    "state" : "1"
                                }
                            }

                            log_data = {
                                "id_acl_master": str(i['cluster-set']['receive']['id_acl_master']),
                                "messages": a['cluster-set'],
                                "command_type": "Add: "+i['cluster-set']['sendblock']['rtype']
                            }
                        db.insert("cs_acl_master_log", log_data)
                        db.update("cs_acl_master", data_state)
                except Exception:
                    pass
                
                cmd.conf_commit_http(server_uri)
                result.append(http_response)
            return response(200, data=result)

        if init_data['action'] == 'slave-notify':
            result = list()
            for i in init_data['data']:
                tags = i['tags']
            respons = cmd.conf_set_notify_slave(tags)
            for i in respons:
                url = i['cluster-set']['receive']['uri']
                url_fix= "http://"+url+":"+i['cluster-set']['receive']['port']
                slave_server_url = url_fix+"/api/command_rest"
                cmd.conf_begin_http(slave_server_url)
                http_response = utils.send_http(slave_server_url,i)
                try:
                    for a in http_response['description']:
                        data_state = None
                        log_data = None
                        if a['cluster-set'] != "OK\n":
                            data_state = {
                                "where":{
                                    "id_notify_slave" : str(i['cluster-set']['receive']['id_notify_slave'])
                                },
                                "data":{
                                    "state" : "0"
                                }
                            }

                            log_data = {
                                "id_notify_slave": str(i['cluster-set']['receive']['id_notify_slave']),
                                "messages": a['cluster-set'],
                                "command_type": "add: "+i['cluster-set']['sendblock']['rtype']
                            }
                        else:
                            data_state = {
                                "where":{
                                    "id_notify_slave" : str(i['cluster-set']['receive']['id_notify_slave'])
                                },
                                "data":{
                                    "state" : "1"
                                }
                            }
                            log_data = {
                                "id_notify_slave": str(i['cluster-set']['receive']['id_notify_slave']),
                                "messages": a['cluster-set'],
                                "command_type": "Add: "+i['cluster-set']['sendblock']['rtype']
                            }
                        db.insert("cs_notify_slave_log", log_data)
                        db.update("cs_notify_slave", data_state)
                except Exception:
                    pass
                
                cmd.conf_commit_http(slave_server_url)
                result.append(http_response)
            return response(200, data=result)

        if init_data['action'] == 'slave-acl':
            result = list()
            for i in init_data['data']:
                tags = i['tags']
            respons = cmd.conf_set_acl_slave(tags)
            for i in respons:
                url = i['cluster-set']['receive']['uri']
                url_fix= "http://"+url+":"+i['cluster-set']['receive']['port']
                slave_server_url = url_fix+"/api/command_rest"
                cmd.conf_begin_http(slave_server_url)
                http_response = utils.send_http(slave_server_url,i)
                try:
                    for a in http_response['description']:
                        data_state = None
                        log_data = None
                        if a['cluster-set'] != "OK\n":
                            data_state = {
                                "where":{
                                    "id_acl_master" : str(i['cluster-set']['receive']['id_acl_master'])
                                },
                                "data":{
                                    "state" : "0"
                                }
                            }
                            log_data = {
                                "id_acl_master": str(i['cluster-set']['receive']['id_acl_master']),
                                "messages": a['cluster-set'],
                                "command_type": "add: "+i['cluster-set']['sendblock']['rtype']
                            }
                        else:
                            data_state = {
                                "where":{
                                    "id_acl_master" : str(i['cluster-set']['receive']['id_acl_master'])
                                },
                                "data":{
                                    "state" : "1"
                                }
                            }
                            log_data = {
                                "id_acl_master": str(i['cluster-set']['receive']['id_acl_master']),
                                "messages": a['cluster-set'],
                                "command_type": "Add: "+i['cluster-set']['sendblock']['rtype']
                            }
                        # db.insert("cs_acl_slave_log", log_data)
                        # db.update("cs_acl_slave", data_state)
                except Exception:
                    pass
                
                cmd.conf_commit_http(slave_server_url)
                result.append(http_response)
            return response(200, data=result)

        if init_data['action'] == 'file-set':
            result = list()
            for i in init_data['data']:
                tags = i['tags']
            respons = cmd.conf_set_file(tags)
            for i in respons:
                url_slave = i['cluster-set']['receive']['slave_uri']
                url_slave_fix= "http://"+url_slave+":"+i['cluster-set']['receive']['slave_port']
                slave_server_url = url_slave_fix+"/api/command_rest"
                url_master = i['cluster-set']['receive']['master_uri']
                url_master_fix= "http://"+url_master+":"+i['cluster-set']['receive']['master_port']
                master_server_url = url_master_fix+"/api/command_rest"
                cmd.conf_begin_http(slave_server_url)
                http_response_slave = utils.send_http(slave_server_url,i)
                cmd.conf_commit_http(slave_server_url)
                result.append(http_response_slave)

                cmd.conf_begin_http(master_server_url)
                http_response = utils.send_http(master_server_url,i)
                cmd.conf_commit_http(master_server_url)
                result.append(http_response)

            return response(200, data=result)



        if init_data['action'] == 'module-set':
            result = list()
            for i in init_data['data']:
                tags = i['tags']
            respons = cmd.conf_set_module(tags)
            for i in respons:
                url_slave = i['cluster-set']['receive']['slave_uri']
                url_slave_fix= "http://"+url_slave+":"+i['cluster-set']['receive']['slave_port']
                slave_server_url = url_slave_fix+"/api/command_rest"
                url_master = i['cluster-set']['receive']['master_uri']
                url_master_fix= "http://"+url_master+":"+i['cluster-set']['receive']['master_port']
                master_server_url = url_master_fix+"/api/command_rest"
                cmd.conf_begin_http(slave_server_url)
                http_response_slave = utils.send_http(slave_server_url,i)
                cmd.conf_commit_http(slave_server_url)
                result.append(http_response_slave)
                
                cmd.conf_begin_http(master_server_url)
                http_response_master = utils.send_http(master_server_url,i)
                cmd.conf_commit_http(master_server_url)
                result.append(http_response_master)
            return response(200, data=result)

        if init_data['action'] == 'cluster-zone':
            result = list()
            for i in init_data['data']:
                tags = i['tags']
            respons = cl_command.cluster_zone(tags)
            return response(200, data=respons)

        # if init_data['action'] == 'cluster-unset':
        #     result = list()
        #     for i in init_data['data']:
        #         tags = i['tags']
        #     respons = cl_command.unset_cluster(tags)
        #     return response(200, data=respons)

        if init_data['action'] == 'cluster':
            result = list()
            for i in init_data['data']:
                tags = i['tags']
            data_master = db.get_all("cs_master")
            for i in data_master:
                master_command = cmd.cluster_command_new(tags, i['nm_config'], "master")
                url_fix= "http://"+i['ip_master']+":"+i['port']
                # url_fix= "http://127.0.0.1:"+i['port']
                master_server_url = url_fix+"/api/command_rest"
                http_response_master = utils.send_http_cl(master_server_url, master_command)
                cl_status = None
                cl_messages = None
                for r in http_response_master:
                    if http_response_master['cluster_report']['serial'] != "OK" and http_response_master['cluster_report']['file'] != "OK" and http_response_master['cluster_report']['module'] != "OK" and http_response_master['cluster_report']['acl'] != "OK" and http_response_master['cluster_report']['notify'] != "OK" and http_response_master['cluster_report']['master'] != "OK":
                        cl_status = True
                        cl_messages = "Clustering "+http_response_master['cluster_report']['description']['cluster-set']['owner']+" "+http_response_master['cluster_report']['description']['cluster-set']['data']
                    else:
                        cl_status = False
                        cl_messages = "Cluster Not Completed"
                result.append({
                    "status": cl_status,
                    "data": http_response_master,
                    "messages": cl_messages,
                    "roles": "master"
                })
            data_slave = db.get_all("v_cs_slave_node")
            for a in data_slave:
                slave_command = cmd.cluster_command_new(tags, a['nm_config'], "slave")
                url_fix= "http://"+a['ip_slave_node']+":"+a['port_slave_node']
                # url_fix= "http://127.0.0.1:"+i['port']
                slave_server_url = url_fix+"/api/command_rest"
                http_response_slave = utils.send_http_cl(slave_server_url, slave_command)
                cl_status = None
                cl_messages = None
                for r in http_response_slave:
                    if http_response_slave['cluster_report']['serial'] != "OK" and http_response_slave['cluster_report']['file'] != "OK" and http_response_slave['cluster_report']['module'] != "OK" and http_response_slave['cluster_report']['acl'] != "OK" and http_response_slave['cluster_report']['notify'] != "OK" and http_response_slave['cluster_report']['master'] != "OK":
                        cl_status = True
                        cl_messages = "Clustering "+http_response_slave['cluster_report']['description']['cluster-set']['owner']+" "+http_response_slave['cluster_report']['description']['cluster-set']['data']
                    else:
                        cl_status = False
                        cl_messages = "Cluster Not Completed"
                result.append({
                    "status": cl_status,
                    "data": http_response_slave,
                    "messages": cl_messages,
                    "roles": "slave"
                })
            return response(200, data=result)

        if init_data['action'] == 'cluster-unset':
            result = list()
            for i in init_data['data']:
                tags = i['tags']
            
            data_master = db.get_all("cs_master")
            for i in data_master:
                master_command = cmd.unset_cluster_command_new(tags)
                url_fix= "http://"+i['ip_master']+":"+i['port']
                master_server_url = url_fix+"/api/command_rest"
                cmd.conf_begin_http(master_server_url)
                http_response_master = utils.send_http(master_server_url, master_command)
                cmd.conf_commit_http(master_server_url)
                result.append(http_response_master)
            # data_slave = db.get_all("v_cs_slave_node")
            # for a in data_slave:
            #     slave_command = cmd.cluster_command_new(tags, a['nm_config'], "slave")
            #     url_fix= "http://"+a['ip_slave_node']+":"+a['port_slave_node']
            #     slave_server_url = url_fix+"/api/command_rest"
            #     http_response_slave = utils.send_http(slave_server_url, slave_command)
                
            return response(200, data=result)

        if init_data['action'] == 'config-file':
            respons = list()
            for i in init_data['data']:
                tags = i['tags']
            try:
                json_begin = cmd.zone_begin_http(url,tags) 
                respons.append(json_begin)
                json_command = cmd.zone_conf_file(tags)
                http_response = utils.send_http(url,json_command)
                respons.append(http_response)
                res_commit = cmd.zone_commit_http(url,tags)
                respons.append(res_commit)
            except Exception as identifier:
                return response(401, message=str(e))
            else:
                return response(200, data=respons)
        


