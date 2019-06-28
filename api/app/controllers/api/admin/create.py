from flask_restful import Resource, reqparse, fields, request
from app.helpers.rest import *
from app.helpers.memcache import *
from app.models import model as db
from app.libs.utils import send_http, change_state, domain_validation
import datetime, os
from app.middlewares.auth import login_required
from app.helpers import command as cmd
from app import redis_store
import dill


url_env = os.environ.get("SOCKET_AGENT_HOST", os.getenv('SOCKET_AGENT_HOST'))
port = os.environ.get("SOCKET_AGENT_PORT", os.getenv('SOCKET_AGENT_PORT'))
url_fix= url_env+":"+port
url = url_fix+"/api/command_rest"

date = datetime.datetime.now().strftime("%Y%m%d")

def sync_conf_insert(id_zone):
    tags = {
        "id_zone" : id_zone
    }
    respons_c_insert = cmd.config_insert(tags)
    cmd.conf_begin_http(url)
    check_res = send_http(url,respons_c_insert)
    if check_res:
        # state change
        state = change_state("id_zone", id_zone, "1")
        check = db.update("zn_zone", data = state)
        print(check)
    cmd.conf_commit_http(url)

def sync_soa(id_zone):
    tags = {
        "id_zone" : id_zone
    }
    cmd.z_begin(url,tags)
    id_record,respons = cmd.zone_soa_insert_default(tags)
    check_res = send_http(url,respons)
    if check_res:
        # state change
        state = change_state("id_record", id_record, "1")
        db.update("zn_record", data = state)

    cmd.z_commit(url, tags)

def sync_ns(id_zone):
    tags = {
        "id_zone" : id_zone
    }
    cmd.z_begin(url, tags)
    result_ns = cmd.zone_ns_insert(tags)
    for i in result_ns:
        check_res = send_http(url, i['command'])
        if check_res:
            state = change_state("id_record", i['id_record'], "1")
            db.update("zn_record", data = state)
    cmd.z_commit(url,tags)

def sync_cname_default(id_zone, id_record):
    tags = {
        "id_record": id_record
    }
    cmd.zone_begin_http(url,tags)
    json_command = cmd.zone_insert(tags)
    check_res = send_http(url,json_command)
    if check_res:
        # state change
        state = change_state("id_record", id_record, "1")
        db.update("zn_record", data = state)
    cmd.zone_commit_http(url,tags)

def addSOADefault(zone):
    zone_data = db.get_by_id("zn_zone","nm_zone", zone)
    type_data = db.get_by_id("zn_type","nm_type","SOA")

    record_soa = {
        "nm_record": '@',
        "date_record": str(date),
        "id_zone":str(zone_data[0]['id_zone']),
        "id_type":str(type_data[0]['id_type'])
    }
    try:
        db.insert("zn_record", record_soa)
    except Exception as e:
        return response(401, message=str(e))

    record_soa_data = db.get_by_id("zn_record","id_zone",zone_data[0]['id_zone'])
    ttldata_soa = {
        "id_record": str(record_soa_data[0]['id_record']),
        "id_ttl": "402140815780249601"
    }

    try:
        db.insert("zn_ttldata", ttldata_soa)
    except Exception as e:
         return response(401, message=str(e))

    ttl_soa_data = db.get_by_id("zn_ttldata","id_record",record_soa_data[0]['id_record'])
    content_soa_d = os.environ.get("DEFAULT_SOA_CONTENT", os.getenv('DEFAULT_SOA_CONTENT'))
    content_soa_d = content_soa_d.split(" ")
    for i in content_soa_d:
        content_soa = {
            "id_ttldata": str(ttl_soa_data[0]['id_ttldata']),
            "nm_content": i
        }
        try:
            db.insert("zn_content", content_soa)
        except Exception as e:
            return response(401, message=str(e))

    serial_content_soa = os.environ.get("DEFAULT_SOA_SERIAL", os.getenv('DEFAULT_SOA_SERIAL'))
    serial_content_soa = serial_content_soa.split(" ")
    for c in serial_content_soa:
        serial_content = {
            "nm_content_serial": c,
            "id_record": str(record_soa_data[0]['id_record'])
        }
        try:
            db.insert("zn_content_serial", serial_content)
        except Exception as e:
            return response(401, message=str(e))
    return str(zone_data[0]['id_zone'])

def addNSDefault(zone):
    zone_data = db.get_by_id("zn_zone","nm_zone", zone)
    type_data = db.get_by_id("zn_type","nm_type","NS")
    
    record_ns = {
        "nm_record": "@",
        "date_record": str(date),
        "id_zone":str(zone_data[0]['id_zone']),
        "id_type":str(type_data[0]['id_type'])
    }

    try:
        db.insert("zn_record", record_ns)
    except Exception as e:
        return response(401, message=str(e))

    record_ns_data = db.get_by_id("zn_record","id_zone",zone_data[0]['id_zone'])
    for i in record_ns_data:
        if str(i['id_type']) ==  "402393625286410241":
            record_ns_data = i
    ttldata_ns = {
        "id_record": str(record_ns_data['id_record']),
        "id_ttl": "402140815780249601"
    }

    try:
        db.insert("zn_ttldata", ttldata_ns)
    except Exception as e:
        return response(401, message=str(e))
    ttl_ns_data = db.get_by_id("zn_ttldata","id_record",str(record_ns_data['id_record']))
    # content = repodefault()['default']['ns']
    content = os.environ.get("DEFAULT_NS", os.getenv('DEFAULT_NS'))
    content = content.split(" ")

    for i in content:
        content_ns = {
            "id_ttldata": str(ttl_ns_data[0]['id_ttldata']),
            "nm_content": i
        }
        try:
            db.insert("zn_content", content_ns)
        except Exception as e:
            return response(401, message=str(e))
    return str(zone_data[0]['id_zone'])

def addCNAMEDefault(id_zone, nm_zone):
    id_record = None
    data_record = {
        "nm_record": "www",
        "date_record":str(date),
        "id_type": "402427533112147969",
        "id_zone": id_zone
    }

    try:
        id_record = db.insert("zn_record", data=data_record)
    except Exception as e:
        return response(401, message=str(e))

    data_ttl = {
        "id_record": id_record,
        "id_ttl": "402140815780249601"
    }

    try:
        id_ttl_data = db.insert("zn_ttldata", data=data_ttl)
    except Exception as e:
        return response(401, message=str(e))

    data_content = {
        "id_ttldata": id_ttl_data,
        "nm_content": nm_zone+"."
    }

    try:
        db.insert("zn_content", data=data_content)
    except Exception as e:
        return response(401, message=str(e))

    return id_record


class CreateDNSAdminRole(Resource):
    @login_required
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('domain', type=str, required=True)
        parser.add_argument('project_id', type=str, required=True)
        args = parser.parse_args()
        project_id = args['project_id']
        zone = args['domain']
        lowercase_zone = zone.lower()
        if not domain_validation(zone):
            return response(401, message="domain name not valid")
        else:
            zone_domain = {
                'nm_zone': lowercase_zone
            }
            data_insert = None

            try:
                data_insert = db.insert("zn_zone", zone_domain)
            except Exception as e:
                return response(401, message=str(e))
            
            userdata = db.get_by_id("userdata", "project_id", str(project_id))
            userdata_id = userdata[0]['userdata_id']
            dt_user_zone = {
                'id_zone': str(data_insert),
                'userdata_id': str(userdata_id)
            }
            db.insert("zn_user_zone", dt_user_zone)

            id_zone_soa = addSOADefault(zone)
            id_zone_ns = addNSDefault(zone)
            id_record = addCNAMEDefault(data_insert, zone)

            # #UNCOMENT TO SYNC AUTO
            sync_conf_insert(data_insert)
            sync_soa(id_zone_soa)
            sync_ns(id_zone_ns)
            sync_cname_default(data_insert, id_record)
            # #UNCOMENT TO SYNC AUTO

            respon = list()

            try:
                zone_data = db.get_by_id("zn_zone","nm_zone", zone)
            except Exception as e:
                # data = {
                #     "status": False,
                #     "messages": str(e)
                # }
                # respon.append(data)
                # return response(200, message=data)
                return response(401, message=str(e))
            else:
                for i in zone_data:
                    data = {
                        'id_zone': str(i['id_zone']),
                        'nm_zone': i['nm_zone'],
                        'state': i['state']
                    }
                respon = {
                    "status": True,
                    "data": data
                }
                return response(200, data=respon,message="Fine!")



