import requests
import json
from libs.utils import get_url,get_time,get_idkey
import copy

with open('libs/templates/endpoints.json', 'r') as f :
    jsonmodel = json.load(f)

def send_request(endpoint,data):
    url = get_url(endpoint)
    try :
        result = requests.post(
            url = url,
            data = json.dumps(data)
        )
        result = result.json()
        respons=result['message']['id']
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
    key = list(data['where']['tags'].keys())[0]
    data['where']['tags'][key] = str(name)
    try :
        res = requests.post(url = url,
        data = json.dumps(data))
        res = res.json()
        res = res['data']
        respons = res[0][get_idkey(endpoint)]
    except Exception as e:
        respons = {
            "status" : False,
            "error"  : str(e)
        }        
    return respons

def setDefaultDns(name):
    
    res = requests.post("http://127.0.0.1:6968/api/user/dnscreate",
    data = {'domain' : str(name)})
    ress = res.json()

    if 'code' not in ress :
        print(ress['message'])

def setRecord(obj):
    
    temp = copy.deepcopy(obj)
    
    data = searchId('zone',obj['--nm-zn'])
    temp['--id-zone'] = data
    data = searchId('type',obj['--type'].upper())
    temp['--id-type'] = data
    data = searchId('ttl',obj['--ttl'])
    temp['--id-ttl'] = data
    
    #insert Record
    json_data = jsonmodel['create']['record']['data']
    for i in json_data['insert']['fields']:
        json_data['insert']['fields'][i] = temp[json_data['insert']['fields'][i]]
    
    temp['--id-record'] = send_request('record',json_data)
    

    #insert ttldata
    json_data = jsonmodel['create']['ttldata']['data']
    for i in json_data['insert']['fields']:
        json_data['insert']['fields'][i] = temp[json_data['insert']['fields'][i]]
    temp['--id-ttldata'] = send_request('ttldata',json_data)
    
    #insert content
    json_data = jsonmodel['create']['content']['data']
    for i in json_data['insert']['fields']:
        json_data['insert']['fields'][i] = temp[json_data['insert']['fields'][i]]
    print(json_data)
    temp['--id-content'] = send_request('content',json_data)   
    
    #insert content serial
    json_data = jsonmodel['create']['content_serial']['data']
    for i in json_data['insert']['fields']:
        json_data['insert']['fields'][i] = temp[json_data['insert']['fields'][i]]
    print(json_data)
    temp['--id-ttldata'] = send_request('content_serial',json_data)


    return data
   