import requests
import json
from libs.utils import get_url,get_time,get_idkey,dictcleanup
from libs.auth import get_headers, get_user_id
import copy

with open('libs/templates/endpoints.json', 'r') as f :
    jsonmodel = json.load(f)
    f.close()

def send_request(endpoint,data):
    headers = get_headers()
    url = get_url(endpoint)
    try :
        result = requests.post(
            url = url,
            data = json.dumps(data),
            headers = headers
        )
        respons = result.json()
    except Exception as e:
        respons = {
            "status" : False,
            "error"  : str(e) + "at " + str(endpoint)
        }    
    return respons

def searchId(endpoint,name):
    data = dict()
    data = jsonmodel['search'][endpoint]['data']
    url = get_url(endpoint)
    keys = list(data['where']['tags'].keys())
    for i in keys:
        if 'id' not in i:
            key = i
    data['where']['tags'][key] = str(name)
    try :
        res = requests.post(url = url,
        data = json.dumps(data),
        headers=get_headers())
        res = res.json()
        res = res['data']
        respons = res[0][get_idkey(endpoint, headers=get_headers())]
    except Exception as e:
        respons = {
            "status" : False,
            "error"  : str(e)
        }        
    return respons

def setDefaultDns(name):
    # if check_alphanumeric:
    #     print('Invalid input')
    #     return False
    
    header = get_headers()
    header['user_id'] = get_user_id()
    res = requests.post("http://127.0.0.1:6968/api/user/dnscreate",
    data = {'domain' : str(name)}
    ,headers=get_headers())
    res = res.json()
    if 'code' not in res :
        print(res['message'])
        return False
    
    tying_zone(header['user_id'],res['data']['data']['id_zone'])

    tags = res['data']['data']['id_zone']
    syncdat = {"command" : "conf-insert", "tags" : str(tags)}
    res=sync(syncdat)
    syncdat = {"command" : "zone-soa-insert", "tags" : str(tags)}
    res=sync(syncdat)
    syncdat = {"command" : "zone-ns-insert", "tags" : str(tags)}
    res=sync(syncdat)

def tying_zone(user_id,id_zone):
    header = get_headers()
    header['user-id'] = str(user_id)
    data = {"id_zone" : str(id_zone)}
    url = get_url('userzone')
    res = requests.post(url = url, data = data, headers = header)

def setRecord(obj):
    from libs.list import check_zone_authorization
    with open('libs/templates/endpoints.json', 'r') as f :
        jsonmodel = json.load(f)


        temp = copy.deepcopy(obj)
        
        check_zone_authorization([obj['--nm-zn']])


        data = searchId('zone',obj['--nm-zn'])
        temp['--id-zone'] = data
        data = searchId('type',obj['--type'].upper())
        temp['--id-type'] = data
        data = searchId('ttl',obj['--ttl'])
        temp['--id-ttl'] = data
        #insert Record
        json_data = copy.deepcopy(jsonmodel['create']['record']['data'])
        for i in json_data['insert']['fields']:
            json_data['insert']['fields'][i] = temp[json_data['insert']['fields'][i]]
        res = send_request('record',json_data)
        temp['--id-record'] = res['message']['id']


        #insert ttldata
        json_data = jsonmodel['create']['ttldata']['data']
        for i in json_data['insert']['fields']:
            json_data['insert']['fields'][i] = temp[json_data['insert']['fields'][i]]
        res = send_request('ttldata',json_data)
        temp['--id-ttldata'] = res['message']['id']
        
        #insert content
        json_data = jsonmodel['create']['content']['data']
        for i in json_data['insert']['fields']:
            json_data['insert']['fields'][i] = temp[json_data['insert']['fields'][i]]
        res = send_request('content',json_data)
        temp['--id-content'] = res['message']['id']

        #insert content serial
        record_type = obj['--type'].upper()

        if record_type == 'SRV' or record_type == 'MX':
            json_data = jsonmodel['create']['content_serial']['data']
            for i in json_data['insert']['fields']:
                json_data['insert']['fields'][i] = temp[json_data['insert']['fields'][i]]
            res = send_request('content_serial',json_data)
            temp['--id-content-serial'] = res['message']['id']
        f.close()

    if record_type == 'MX':
        cmd = 'zone-mx-insert'
        datasync = {"command" : cmd, "tags" : temp['--id-zone']}
    elif record_type == 'SRV':
        cmd = 'zone-srv-insert'
        datasync = {"command" : cmd, "tags" : temp['--id-zone']}
    else :
        cmd = 'zone-insert'
        datasync = {"command" : cmd, "tags" : temp['--id-record']}

    try:
        sync(datasync)
    except Exception as e:
        print("Error \n",str(e))

    return data


def remove_data(name,endpoint):
    json_data = jsonmodel['rm'][endpoint]['data']
    url = get_url(endpoint)
    key = get_idkey(endpoint, headers=get_headers())
    delid = searchId(endpoint,name)
    json_data['remove']['tags'][key] = delid
    try :
        requests.post(url, data = json.dumps(json_data)
        , headers=get_headers())
    except Exception as e:
        respons = str(e)
        print(respons)
    return

def sync(obj):
    cmd = obj['command']
    tags = obj['tags']
    data_send = {cmd : {"tags" : ''}}
    
    if cmd != 'zone-insert':
        data_send[cmd]['tags'] =  {"id_zone" : tags}
    else :
        data_send[cmd]['tags'] = {"id_record" : tags}
        
    res=send_request('command', data_send)
    
    return res
    