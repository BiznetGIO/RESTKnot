from flask_restful import Resource, reqparse, request
from app.helpers.rest import response
from app.helpers import cmd_parser as cmd
from app import psycopg2,db
from app.libs import utils
from app.models import model

class Content(Resource):
    ##@jwt_required
    def get(self):
        command = utils.get_command(request.path)
        command = "zn_"+command
        try:
            results = model.get_all(command)
        except Exception:
            results = None
        else:
            obj_userdata = list()
            for i in results :
                data = {
                    "id_content": str(i['id_content']),
                    "id_ttldata": str(i['id_ttldata']),
                    "nm_content": str(i['nm_content'])
                }
                obj_userdata.append(data)
            return response(200, data=obj_userdata)

    ##@jwt_required
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
                result = model.insert(table, fields)
            except Exception as e:
                respons = {
                    "status": False,
                    "error": str(e)
                }
            else:
                respons = {
                    "status": True,
                    "messages": "Fine!",
                    "id": result
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
                        "id_content": str(i['id_content']),
                        "id_ttldata": str(i['id_ttldata']),
                        "nm_content": str(i['nm_content'])
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
                for a in tags:
                    if tags[a] is not None:
                        fields = a
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
            column = model.get_columns("v_contentdata")
            try:
                result = list()
                if fields is None:
                    query = """select * from v_contentdata"""
                    db.execute(query)
                    rows = db.fetchall()
                    for row in rows:
                        result.append(dict(zip(column, row)))
                else:
                    query = """ select * from v_contentdata where """+fields+"""='"""+tags[fields]+"""'"""
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
                        "id_content": str(i['id_content']),
                        "nm_zone": str(i['nm_zone']),
                        "nm_record": str(i['nm_record']),
                        "nm_type" : str(i['nm_type']),
                        "nm_ttl" : i['nm_ttl'],
                        "id_record" : str(i['id_record']),
                        "nm_content": str(i['nm_content']),
                    }
                    obj_userdata.append(data)
                respons = {
                    "status": True,
                    "messages": "Fine!"
                }
            finally:
                return response(200, data=obj_userdata , message=respons)