import json
import requests

def getId(name,endpoint,tokentest):
    url = 'http://127.0.0.1:6968/api/'+endpoint
    val = name
    key = 'nm_'+endpoint
    id_key = 'id_'+endpoint
    res = requests.request("GET",url=url,headers = tokentest)
    data = res.json()
    return_id = ''
    for i in data['data']:
        if(i[key] == val):
            return_id = i[id_key]
    
    return return_id
