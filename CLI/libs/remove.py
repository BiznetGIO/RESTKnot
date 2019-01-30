import json
import requests
from libs import config as app
from libs import utils as util
from libs import list as ls
from libs import auth

with open('libs/templates/endpoints.json','r') as model :
    jsonmodel = json.load(model)


def remove_zone(zone):
    json_send = jsonmodel['rm']['zone']['data']
    id_zone = ls.get_data('zone', key='id_zone', tags='nm_zone', value=zone)
    id_zone = id_zone['data'][0]
    json_send['remove']['tags']['id_zone'] = id_zone
    try :
        res = app.send_request('zone', json_send)
    except Exception as e:
        util.log_err(e)
    finally :
        return res

def remove_record(records):
        json_send = jsonmodel['rm']['record']['data']
        result=list()
        for i in records:
            json_send = jsonmodel['rm']['record']['data']
            json_send['remove']['tags']['id_record'] = i
            try :
                res = app.send_request('record', json_send)
                result.append(res)
            except Exception as e:
                util.log_err(e)
        return result

        