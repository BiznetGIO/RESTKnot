import json
import requests
import datetime
import tabulate
import coloredlogs
import logging
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit import prompt


with open('libs/templates/var.json','r') as f :
    var_json = json.load(f)


def check_existence(endpoint,var):
    url = get_url(endpoint)
    key = var_json['key'][endpoint]

    result = requests.get(url)
    result = result.json()
    result = result['data']
    for i in result:
        if i[key] == var:
            respons = True
            break
        else :
            respons = False
    return respons

def get_url(endpoint):
    url = "http://127.0.0.1:6968/api/"

    url = url + var_json['endpoints'][endpoint]

    return url

def get_idkey(endpoint):
    url = get_url(endpoint)
    res = requests.get(url)
    data = res.json()
    data = data['data']
    idname = var_json['id'][endpoint]
       
    return idname



def eleminator(obj):
    delkeys = list()
    for i in obj:
        if obj[i] is None or obj[i] is False :
            delkeys.append(i)
    
    for i in delkeys:
        obj.pop(i)
    
    return obj
        
def get_time():
    now = datetime.datetime.now()
    res = now.strftime("%Y%m%d%H")
    return res


def log_err(stdin):
    coloredlogs.install()
    logging.error(stdin)    

