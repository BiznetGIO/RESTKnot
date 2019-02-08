import json
import requests
import tqdm
from tqdm import tqdm
from libs import config as app
from libs import utils as util
from libs import listing as ls
from libs import auth

with open('libs/templates/endpoints.json','r') as model :
    jsonmodel = json.load(model)


def remove_zone(zone):
    pbar=tqdm(total=100)
    pbar.set_description("Obtaining DNS Data")
    json_send = jsonmodel['rm']['zone']['data']
    pbar.update(10)
    id_zone = ls.get_data('zone', key='id_zone', tags='nm_zone', value=zone)
    pbar.update(20)
    id_zone = id_zone['data'][0]
    pbar.update(10)
    json_send['remove']['tags']['id_zone'] = id_zone
    pbar.update(10)
    try :
        pbar.set_description("Removing DNS")
        res = app.send_request('zone', json_send)
        pbar.update(50)
        pbar.close()
    except Exception as e:
        util.log_err(e)
    finally :
        return res

def remove_record(records):
        json_send = jsonmodel['rm']['record']['data']
        result=list()
        pbar=tqdm(total=100)
        step = (100/(len(records)))
        for i in records:
            pbar.set_description("Removing Record Index - {}".format(records.index(i)))
            json_send = jsonmodel['rm']['record']['data']
            json_send['remove']['tags']['id_record'] = i
            try :
                res = app.send_request('record', json_send)
                result.append(res)
                pbar.update(step)
            except Exception as e:
                util.log_err(e)
        pbar.close()
        return result

        