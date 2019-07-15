from flask_restful import Resource, reqparse, request
from app.helpers.rest import response
from app.helpers import cmd_parser as cmd
from app import psycopg2,db
from app.libs import utils
from app.models import model
from app.middlewares.auth import login_required
from app.helpers import command as syncron
import os

class Record(Resource):
    def get(self):
        command = utils.get_command(request.path)
        command = "zn_"+command
        try:
            results = model.get_all(command)
            obj_userdata = list()
            for i in results :
                data = {
                    "id_record": str(i['id_record']),
                    "id_zone": str(i['id_zone']),
                    "id_type": str(i['id_type']),
                    "nm_record": str(i['nm_record']),
                    "date_record" : i['date_record'],
                    "state" : i['state'] 
                }
                obj_userdata.append(data)
        except Exception:
            results = None
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
            if not utils.record_validation(fields['nm_record']):
                return response(401, message="Record Name Not Valid")
            else:
                l_name = fields['nm_record']
                lower_name = l_name.lower()
                total = 0
                if lower_name.find("."):
                    spl_name = lower_name.split(".")
                    for i in spl_name:
                        if len(i) >= 64:
                            return response(401, message="Record name not valid | front of point 64 characters")
                        else:
                            total = total + len(i)
                    if total >= 255:
                        return response(401, message="Record name not valid | Total record char 255 characters")
                record_checks = False
                try:
                    typename = model.get_by_id("zn_type", "id_type", fields['id_type'])[0]
                except Exception as e:
                    return response(401, message=str(e))
                if typename['nm_type'] == 'CNAME':
                    try:
                        query = "select * from v_record where (nm_type='"+typename['nm_type']+"' and nm_record='"+lower_name+"') and id_zone='"+str(fields['id_zone'])+"'"
                        db.execute(query)
                        adata =db.fetchone()
                    except (Exception, psycopg2.DatabaseError) as e:
                        return response(401, message=(str(e)))
                    else:
                        if adata is not None:
                            record_checks = True

                if record_checks:
                    return response(401, message="duplicate error")
                
                field_fix = {
                    "nm_record": lower_name,
                    "date_record": fields['date_record'],
                    "id_zone":fields['id_zone'],
                    "id_type": fields['id_type']
                }
                try:
                    result = model.insert(table, field_fix)
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
            json_data = init_data['data']
            tags = None
            fields = None
            for i in json_data:
                tags = i['tags']
                fields = i['fields']
            if not utils.record_validation(fields['nm_record']):
                return response(401, message="Record Name Not Valid")
            else:
                l_name = fields['nm_record']
                lower_name = l_name.lower()
                total = 0
                if lower_name.find("."):
                    spl_name = lower_name.split(".")
                    for i in spl_name:
                        if len(i) >= 64:
                            return response(401, message="Record name not valid | front of point 64 characters")
                        else:
                            total = total + len(i)
                    if total >= 255:
                        return response(401, message="Record name not valid | Total record char 255 characters")
                record_checks = False
            
                try:
                    typename = model.get_by_id("zn_type", "id_type", fields['id_type'])[0]
                except Exception as e:
                    return response(401, message=str(e))
                if typename['nm_type'] == 'CNAME':
                    try:
                        query = "select * from v_record where (nm_type='"+typename['nm_type']+"' and nm_record='"+lower_name+"') and id_zone='"+str(fields['id_zone'])+"'"
                        db.execute(query)
                        adata =db.fetchone()
                    except (Exception, psycopg2.DatabaseError) as e:
                        return response(401, message=(str(e)))
                    else:
                        if adata is not None:
                            if str(adata[0]) == tags['id_record']:
                                record_checks = False
                            else:
                                record_checks = True

                if record_checks:
                    return response(401, message="duplicate error")
                msg_plus = ""                       
                syncron.zone_begin_http(url, tags)
                try:
                    data_unset = syncron.zone_unset(tags)
                    a = utils.send_http(url, data_unset)
                except Exception as e:
                    syncron.zone_commit_http(url, tags)
                    return response(401, message="Record Not Unset | "+str(e))
                
                data_edits = {
                    "where":{
                        "id_record": tags['id_record']
                    },
                    "data":{
                        "nm_record": lower_name,
                        "date_record": fields['date_record'],
                        "id_type": fields['id_type'],
                        "id_zone": fields['id_zone']
                    }
                }
            
                try:
                    result = model.update(table, data_edits)
                except Exception as e:
                    syncron.zone_commit_http(url, tags)
                    return response(401, message=str(e))
                else:
                    respons = {
                        "status": result,
                        "messages": "Record Edited"+msg_plus,
                        "id": tags['id_record'],
                    }
                    syncron.zone_commit_http(url, tags)
                    return response(200, data=data_edits['data'] , message=respons)
            
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
                return response(401, message=str(e))
            else:
                for i in result :
                    data = {
                        "id_record": str(i['id_record']),
                        "id_zone": str(i['id_zone']),
                        "id_type": str(i['id_type']),
                        "nm_record": str(i['nm_record']),
                        "date_record" : i['date_record'],
                        "state" : i['state'] 
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
                return response(401, message=str(e))
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
            column = model.get_columns("v_record")
            try:
                result = list()
                if fields is None:
                    query = """select * from v_record"""
                    db.execute(query)
                    rows = db.fetchall()
                    for row in rows:
                        result.append(dict(zip(column, row)))
                else:
                    query = """ select * from v_record where """+fields+"""='"""+tags[fields]+"""'"""
                    db.execute(query)
                    rows = db.fetchall()
                    for row in rows:
                        result.append(dict(zip(column, row)))
            except Exception as e:
                return response(401, message=str(e))
            else:
                for i in result :
                    data = {
                        "id_record": str(i['id_record']),
                        "nm_zone": str(i['nm_zone']),
                        "nm_type": str(i['nm_type']),
                        "nm_record": str(i['nm_record']),
                        "date_record" : i['date_record'],
                        "state" : i['state'] 
                    }
                    obj_userdata.append(data)
                respons = {
                    "status": True,
                    "messages": "Fine!"
                }
                return response(200, data=obj_userdata , message=respons)
        
        if init_data['action'] == 'view_all':
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
            column_2 = model.get_columns("v_content_serial")
            column_2 = column + column_2
            try:
                result = list()
                result_2 = list()
                if fields is None:
                    query = """select * from v_contentdata"""
                    query_2 = """select * from v_contentdata m1 join v_content_serial m2 on m1.id_record=m2.id_record"""
                    db.execute(query)
                    rows = db.fetchall()
                    db.execute(query_2)
                    rows_2 = db.fetchall()
                    for row in rows:
                        result.append(dict(zip(column, row)))
                    for row in rows_2:
                        result_2.append(dict(zip(column_2,row)))
                        
                else:
                    query = """ select * from v_contentdata where """+fields+"""='"""+tags[fields]+"""'"""
                    db.execute(query)
                    rows = db.fetchall()
                    query_2 = """select * from v_contentdata m1 join v_content_serial m2 on m1.id_record=m2.id_record"""
                    db.execute(query_2)
                    rows_2 = db.fetchall()
                    for row in rows_2:
                        result_2.append(dict(zip(column_2,row)))
                    for row in rows:
                        result.append(dict(zip(column, row)))
            except Exception as e:
                return response(401, message=str(e))
            else:
                for i in result :
                    rtype = str(i['nm_type'])
                    tmp_id_record = str(i["id_record"])
                    data = {
                        "id_content": str(i['id_content']),
                        "nm_zone": str(i['nm_zone']),
                        "nm_record": str(i['nm_record']),
                        "nm_type" : str(i['nm_type']),
                        "nm_ttl" : i['nm_ttl'],
                        "id_record" : str(i['id_record']),
                        "nm_content": str(i['nm_content']),
                    }
                    if rtype == 'MX' or rtype == 'SRV':
                        for index_ in result_2:
                            if str(index_["id_record"]) == tmp_id_record:
                                data_2 = {
                                    "id_content_serial": str(index_["id_record"]),
                                    "nm_content_serial": str(index_["nm_content_serial"])
                                }
                        data = {**data, **data_2}
                    obj_userdata.append(data)
                respons = {
                    "status": True,
                    "messages": "Fine!"
                }
                return response(200, data=obj_userdata , message=respons)

        # if init_data['action'] == 'edit':
        #     obj_userdata = list()
        #     table = ""
        #     fields = None
        #     tags = dict()
        #     for i in init_data['data']:
        #         table = i['table']
        #         tags = i['tags']
        #         for a in tags:
        #             if tags[a] is not None:
        #                 fields = a
        #     column = model.get_columns("v_contentdata")
        #     try:
        #         result = list()
        #         if fields is None:
        #             query = """select * from v_contentdata"""
        #             db.execute(query)
        #             rows = db.fetchall()
        #             for row in rows:
        #                 result.append(dict(zip(column, row)))
        #         else:
        #             query = """ select * from v_record where """+fields+"""='"""+tags[fields]+"""'"""
        #             db.execute(query)
        #             rows = db.fetchall()
        #             for row in rows:
        #                 result.append(dict(zip(column, row)))
        #     except Exception as e:
        #         return response(401, message=str(e))
        #     else:
        #         for i in result :
        #             data = {
        #                 "id_record": str(i['id_record']),
        #                 "nm_zone": str(i['nm_zone']),
        #                 "nm_type": str(i['nm_type']),
        #                 "nm_record": str(i['nm_record']),
        #                 "date_record" : i['date_record'],
        #                 "state" : i['state'] 
        #             }
        #             obj_userdata.append(data)
        #         respons = {
        #             "status": True,
        #             "messages": "Fine!"
        #         }
        #         return response(200, data=obj_userdata , message=respons)