from flask_restful import Resource, reqparse, request
from app.helpers.rest import response
from app.helpers import cmd_parser as cmd
from app import psycopg2,db
from app.libs import utils
from app.models import model
from app.middlewares.auth import login_required


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
                if typename['nm_type'] == 'CNAME' or typename['nm_type'] == 'MX':
                    try:
                        query = "select * from v_record where (nm_type='"+typename+"' and nm_record='"+lower_name+"') and id_zone='"+str(fields['id_zone'])+"'"
                        db.execute(query)
                        adata =db.fetchone()
                    except (Exception, psycopg2.DatabaseError) as e:
                        return response(401, message=(str(e)))
                    else:
                        print(adata)
                        if adata is not None:
                            record_checks = True

                if record_checks:
                    return response(401, message="Record name not valid")
                
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