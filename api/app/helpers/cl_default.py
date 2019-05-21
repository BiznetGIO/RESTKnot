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

def sync_conf_unset(url, id_zone):
    tags = {
        "id_zone" : id_zone
    }
    respons_c_insert = cmd.conf_unset(tags)
    cmd.conf_begin_http(url)
    res = send_http(url,respons_c_insert)
    cmd.conf_commit_http(url)
    return res

