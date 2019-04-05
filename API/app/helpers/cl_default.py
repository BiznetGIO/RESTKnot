from app.helpers import command as cmd
from app import redis_store
import dill
from app.models import model as db
from app.libs.utils import send_http
import datetime, json


date = datetime.datetime.now().strftime("%Y%m%d%H")
def sync_conf_insert(url, id_zone):
    tags = {
        "id_zone" : id_zone
    }
    respons_c_insert = cmd.config_insert(tags)
    cmd.conf_begin_http(url)
    res = send_http(url,respons_c_insert)
    cmd.conf_commit_http(url)
    return res

def sync_soa(url,id_zone):
    tags = {
        "id_zone" : id_zone
    }
    cmd.z_begin(url,tags)
    _,respons = cmd.zone_soa_insert_default(tags)
    check_res = send_http(url,respons)
    cmd.z_commit(url, tags)
    return check_res

def sync_ns(url, id_zone):
    res = list()
    tags = {
        "id_zone" : id_zone
    }
    cmd.z_begin(url, tags)
    result_ns = cmd.zone_ns_insert(tags)
    for i in result_ns:
        check_res = send_http(url, i['command'])
        res.append(check_res)
    cmd.z_commit(url,tags)
    return res

def sync_cname_default(url, id_zone, id_record):
    tags = {
        "id_record": id_record
    }
    cmd.zone_begin_http(url,tags)
    json_command = cmd.zone_insert(tags)
    check_res = send_http(url,json_command)
    cmd.zone_commit_http(url,tags)
    return check_res

