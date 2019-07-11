from flask_restful import Resource, reqparse, request
from app.helpers.rest import response
from app.helpers import cmd_parser as cmd
from app import psycopg2,db
from app.libs import utils
from app.models import model
from app.middlewares.auth import login_required
from app.helpers import command as syncron
import os


class TtlData(Resource):
    @login_required
    def get(self):
        command = utils.get_command(request.path)
        command = "zn_"+command
        try:
            results = model.get_all(command)
            obj_userdata = list()
            for i in results :
                data = {
                    "id_ttldata": str(i['id_ttldata']),
                    "id_record": str(i['id_record']),
                    "id_ttl": str(i['id_ttl'])
                }
                obj_userdata.append(data)
        except Exception as e:
            return response(401, message=str(e))
        else:
            return response(200, data=obj_userdata)

    @login_required
    def post(self):
        json_req = request.get_json(force=True)
        command = utils.get_command(request.path)
        command = "zn_"+command
        init_data = cmd.parser(json_req, command)
        respons = dict()

        url_env = os.environ.get("SOCKET_AGENT_HOST", os.getenv('SOCKET_AGENT_HOST'))
        port = os.environ.get("SOCKET_AGENT_PORT", os.getenv('SOCKET_AGENT_PORT'))
        url_fix= url_env+":"+port
        url = url_fix+"/api/command_rest"

        if init_data['action'] == 'insert':
            table = init_data['data'][0]['table']
            fields = init_data['data'][0]['fields']
            try:
                result = model.insert(table, fields)
            except Exception as e:
                return response(401, message=str(e))
            else:
                respons = {
                    "status": True,
                    "messages": "Fine!",
                    "id": result
                }
                return response(200, data=fields , message=respons)
    
        if init_data['action'] == 'edit':
            table = init_data['data'][0]['table']
            tags = init_data['data'][0]['tags']
            fields = init_data['data'][0]['fields']
            data_edits = {
                "where": {
                    "id_ttldata": tags['id_ttldata']
                },
                "data" : {
                    "id_record": fields['id_record'],
                    "id_ttl": fields['id_ttl']
                }
            }
            tags_zone = {
                "id_record": fields['id_record']
            }
            syncron.zone_begin_http(url, tags_zone)
            try:
                data_unset = syncron.zone_unset(tags_zone)
                utils.send_http(url, data_unset)
            except Exception as e:
                syncron.zone_commit_http(url, tags_zone)
                return response(401, message="Record Not Unset | "+str(e))
            try:
                result = model.update(table, data_edits)
            except Exception as e:
                syncron.zone_commit_http(url, tags_zone)
                return response(401, message=str(e))
            else:
                respons = {
                    "status": result,
                    "messages": "ttldata edited",
                    "id": tags['id_ttldata']
                }
                syncron.zone_commit_http(url, tags_zone)
                return response(200, data=fields , message=respons)

        if init_data['action'] == 'where':
            obj_userdata = list()
            table = ""
            fields = ""
            tags = dict()
            for i in init_data['data']:
                table = i['table']
                tags = i['tags']
                for a in tags:
                    if tags[a] is not None:
                        fields = a
            try:
                result = model.get_by_id(table,fields,tags[fields])
            except Exception as e:
                respons = {
                    "status": False,
                    "messages": str(e)
                }
            else:
                for i in result :
                    data = {
                        "id_ttldata": str(i['id_ttldata']),
                        "id_record": str(i['id_record']),
                        "id_ttl": str(i['id_ttl'])
                    }
                    obj_userdata.append(data)
                respons = {
                    "status": True,
                    "messages": "Fine!"
                }
            finally:
                return response(200, data=obj_userdata , message=respons)
        if init_data['action'] == 'remove':
            table = ""
            tags = dict()
            fields = ""
            for i in init_data['data']:
                table = i['table']
                tags = i['tags']
            fields = str(list(tags.keys())[0])
            try:
                result = model.delete(table,fields,tags[fields])
            except Exception as e:
                respons = {
                    "status": False,
                    "messages": str(e)
                }
            else:
                respons = {
                    "status": result,
                    "messages": "Fine Deleted!"
                }
            finally:
                return response(200, data=tags, message=respons)

        if init_data['action'] == 'view':
            obj_userdata = list()
            table = ""
            fields = None
            tags = dict()
            for i in init_data['data']:
                table = i['table']
                tags = i['tags']
                for a in tags:
                    if tags[a] is not None:
                        fields = a
            column = model.get_columns("v_ttldata")
            try:
                result = list()
                if fields is None:
                    query = """select * from v_ttldata"""
                    db.execute(query)
                    rows = db.fetchall()
                    for row in rows:
                        result.append(dict(zip(column, row)))
                else:
                    query = """ select * from v_ttldata where """+fields+"""='"""+tags[fields]+"""'"""
                    db.execute(query)
                    rows = db.fetchall()
                    for row in rows:
                        result.append(dict(zip(column, row)))
            except Exception as e:
                respons = {
                    "status": False,
                    "messages": str(e)
                }
            else:
                for i in result :
                    data = {
                        "id_ttldata": str(i['id_ttldata']),
                        "id_ttl": str(i['id_ttl']),
                        "nm_ttl" : i['nm_ttl'],
                        "nm_zone": str(i['nm_zone']),
                        "nm_record": str(i['nm_record']),
                    }
                    obj_userdata.append(data)
                respons = {
                    "status": True,
                    "messages": "Fine!"
                }
            finally:
                return response(200, data=obj_userdata , message=respons)
