from flask_restful import Resource, reqparse, request
from app.helpers.rest import response
from app.helpers import cmd_parser as cmd
from app import psycopg2,db
from app.libs import utils
from app.models import model
from app.middlewares.auth import login_required
from app.helpers import command as syncron
import os


class Content(Resource):
    ##@jwt_required
    @login_required
    def get(self):
        command = utils.get_command(request.path)
        command = "zn_"+command
        try:
            results = model.get_all(command)
        except Exception as e:
            return response(401 ,message=str(e))
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
            ct_rep = fields['nm_content']
            ct_replace = ct_rep.replace("'","''")
            lower_text_data = ct_replace.lower()
            fields_fix = {
                'id_ttldata': fields['id_ttldata'],
                'nm_content': lower_text_data
            }
            try:
                result = model.insert(table, fields_fix)
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
            content_validation = model.get_by_id("v_contentdata", field="id_content", value=str(result))
            check_validation = False
            check_validation_char = None
            if content_validation[0]['nm_type'] == 'A':
                check_validation = utils.a_record_validation(content_validation[0]['nm_content'])
            elif content_validation[0]['nm_type'] == 'CNAME':
                check_validation = utils.cname_validation(content_validation[0]['nm_content'])
                cs_data_name = content_validation[0]['nm_content']
                total = 0
                if cs_data_name.find("."):
                    spl_name = cs_data_name.split(".")
                    for i in spl_name:                       
                        if len(i) >= 64:
                            print(i)
                            check_validation_char = True
                        else:
                            total = total + len(i)
                    if total >= 255:
                        check_validation_char = True

            elif content_validation[0]['nm_type'] == 'NS':
                check_validation = utils.cname_validation(content_validation[0]['nm_content'])
            elif content_validation[0]['nm_type'] == 'TXT':
                check_validation = utils.txt_validation(content_validation[0]['nm_content'])
            # elif content_validation[0]['nm_type'] == 'SRV':
            #     pass
            else:
                check_validation = True

            if check_validation_char:
                model.delete("zn_record", "id_record", str(content_validation[0]['id_record']))
                return response(401, message="Value Not Valid")
            if not check_validation:
                model.delete("zn_record", "id_record", str(content_validation[0]['id_record']))
                return response(401, message="Value Not Valid")
            else:
                return response(200, data=fields , message=respons)
        
        if init_data['action'] == 'edit':
            table = init_data['data'][0]['table']
            tags = init_data['data'][0]['tags']
            fields = init_data['data'][0]['fields']
            ct_rep = fields['nm_content']
            ct_replace = ct_rep.replace("'","''")
            lower_text_data = ct_replace.lower()            
            content_validation = model.get_by_id("v_contentdata", field="id_content", value=tags['id_content'])
            check_validation = False
            check_validation_char = None
            if content_validation[0]['nm_type'] == 'A':
                check_validation = utils.a_record_validation(lower_text_data)
            elif content_validation[0]['nm_type'] == 'CNAME':
                check_validation = utils.cname_validation(lower_text_data)
                cs_data_name = lower_text_data
                total = 0
                if cs_data_name.find("."):
                    spl_name = cs_data_name.split(".")
                    for i in spl_name:                       
                        if len(i) >= 64:
                            check_validation_char = True
                        else:
                            total = total + len(i)
                    if total >= 255:
                        check_validation_char = True

            elif content_validation[0]['nm_type'] == 'NS':
                check_validation = utils.cname_validation(lower_text_data)
            elif content_validation[0]['nm_type'] == 'TXT':
                check_validation = utils.txt_validation(lower_text_data)
            # elif content_validation[0]['nm_type'] == 'SRV':
            #     pass
            else:
                check_validation = True
            if check_validation_char:
                return response(401, message="Value Not Valid")
            if not check_validation:
                return response(401, message="Value Not Valid")
            data_edits = {
                "where":{
                    "id_content": tags['id_content']
                },
                "data":{
                    "nm_content": lower_text_data
                }
            }

            tags_zone = {
                "id_record": str(content_validation[0]['id_record'])
            }
            syncron.zone_begin_http(url, tags_zone)
            try:
                data_unset = syncron.zone_unset(tags_zone)
                utils.send_http(url, data_unset)
            except Exception as e:
                syncron.zone_commit_http(url, tags_zone)
                return response(401, message="Record Not Unset | "+str(e))
            
            try:
                # if check_validation and check_validation_char
                result = model.update(table, data_edits)
            except Exception as e:
                syncron.zone_commit_http(url, tags_zone)
                return response(401, message=str(e))
            else:
                respons = {
                    "status": result,
                    "messages": "Fine!",
                    "id": tags['id_content']
                }
                syncron.zone_commit_http(url, tags_zone)
                return response(200, data=data_edits['data'], message=respons)


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
                return response(401 ,message=str(e))
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
                return response(401 ,message=str(e))
            else:
                respons = {
                    "status": result,
                    "messages": "Fine Deleted!"
                }
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
                return response(401 ,message=str(e))
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
                return response(200, data=obj_userdata , message=respons)