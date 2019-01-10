import json
import requests
import datetime

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








    



# def get_data(zn_nm,zn_type,zn_ttl,args):
#     # GET ACTIVE USER HERE

#     zn_data = dict()
#     fields = dict()

#     if args == "create" :
#         cmd_json = 'insert'
#         zn_data[cmd_json] = dict()
#         if zn_nm is not None:
#             fields['nm_zone'] = zn_nm
#             zn_data[cmd_json]['fields']=fields    
#     elif args == "rm" :
#         cmd_json = 'remove'
#         zn_data[cmd_json] = dict()
#         if zn_nm is not None:
#             fields['id_zone'] = get_id('zone',zn_nm)
#             zn_data[cmd_json]['tags'] = fields
#     elif args == "ls" :
#         cmd_json = 'where'
#         zn_data[cmd_json] = dict()
#         if zn_nm is not None:
#             fields['id_zone'] = get_id('zone',zn_nm)
#             zn_data[cmd_json]['tags'] = fields

#     return zn_data
           
            