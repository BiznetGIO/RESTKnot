from flask_restful import Resource, reqparse, request
from app.helpers.rest import response
from app.helpers import cmd_parser as cmd
from app import psycopg2
from app.libs import utils
from app.models import model as db


class ZoneName(Resource):
    def get(self):
        command = utils.get_command(request.path)
        command = "zn_"+command
        try:
            results = db.get_all(command)
            obj_userdata = list()
            for i in results :
                data = {
                    "id_zone": str(i['id_zone']),
                    "nm_zone" : i['nm_zone']
                }
                obj_userdata.append(data)
        except Exception:
            results = None
        else:
            return response(200, data=obj_userdata)


    def post(self):
        json_req = request.get_json(force=True)
        command = utils.get_command(request.path)
        command = "zn_"+command
        init_data = cmd.parser(json_req, command)
        respons = dict()
        if init_data['action'] == 'insert':
            table = init_data['data'][0]['table']
            fields = init_data['data'][0]['fields']
            try:
                db.insert(table, fields)
            except Exception as e:
                respons = {
                    "status": False,
                    "error": str(e)
                }
            else:
                respons = {
                    "status": True,
                    "messages": "Fine!"
                }
            finally:
                return response(200, data=fields , message=respons)
        if init_data['action'] == 'where':
            obj_userdata = list()
            table = ""
            fields = ""
            tags = dict()
            for i in init_data['data']:
                table = i['table']
                tags = i['tags']
            fields = str(list(tags.keys())[0])
            try:
                result = db.get_by_id(table,fields,tags[fields])
            except Exception as e:
                respons = {
                    "status": False,
                    "messages": str(e)
                }
            else:
                for i in result :
                    data = {
                        "id_zone": str(i['id_zone']),
                        "nm_zone" : i['nm_zone']
                    }
                    obj_userdata.append(data)
                respons = {
                    "status": True,
                    "messages": False
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
                result = db.delete(table,fields,tags[fields])
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