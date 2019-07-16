import json
import requests


class setupData:
	url = {
			"zone"  : "zone",
			"ttl"   : "ttl",
			"type"  : "type",
			"record": "record",
			"ttldata":"ttldata",
			"content":"content",
			"content_serial":"content_serial",
			"user"  : "user",
			"command": "sendcommand",
			"login" :  "login",
			"userzone": "userzone"}
	
	model = {   
			"add" : {"insert" : {"fields" : {}}},
			"remove" : {"remove" : {"tags"  : {}}},
			"where" : {"where" : {"tags" : {}}},
            "view" : {"view" : {"tags" : {}}}
	}
        



def get_id(endpoint,data,headers):
    url = get_url(endpoint)
    send = get_model("where",data)
    send = json.dumps(send)
    result = requests.post(url=url,data=send,headers=headers)
    result = result.json()
    return result['data']

def post_data(endpoint,data,headers):
    url = get_url(endpoint)
    data = json.dumps(data)
    result = requests.post(url=str(url),data=data,headers=headers)
    result = result.json()
    return result

def get_url(endpoint):
    data = setupData()
    url = "http://127.0.0.1:6968/api/"+data.url[endpoint]
    return url

def get_model(model,data):
    json_model = setupData()
    d_model = json_model.model[model]
    for i in d_model:
        for j in d_model[i]:
            if d_model[i][j]:
                d_model[i][j].clear()
            d_model[i][j] = data
    return d_model

    