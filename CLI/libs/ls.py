import json
import requests
from libs import auth
from libs import config
from libs import utils as util

with open('libs/templates/endpoints.json','r') as model :
    jsonmodel = json.load(model)

def listing_endpoint(endpoint):
    with open('libs/templates/var.json','r') as f :
        var_json = json.load(f)
    url = util.get_url(endpoint)
    result = requests.get(url, headers=auth.get_headers())
    result = result.json()
    result = result['data']
    key = var_json['key'][endpoint]
    st = ''
    if result:
        for i in result:
            st += i[key]+'\t'
    else :
        "No value available"
    return st

def get_data(endpoint,headers,key=None):
    url = util.get_url(endpoint)
    try:
        res = requests.get(url = url, headers = headers )
        res = res.json()
        res = res['data']

        if key != None:
            data = list()
            for i in res:
                data.append(i[key])
        else :
            data = res
        
        return data

    except Exception as e:
        util.log_err(e)

def list_dns():
    headers = auth.get_headers()
    headers['user-id'] = auth.get_user_id()
    id_zone = get_data('userzone',headers,'id_zone')
    data = jsonmodel['search']['zone']['data']
    st = ''
    for i in id_zone:
        data['where']['tags']['id_zone'] = i
        temp = config.send_request('zone', data= data, headers=headers)
        temp = temp['data'][0]['nm_zone']
        st += temp +'\t\t\t'
    return st