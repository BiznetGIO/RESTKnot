import json
import requests
import datetime
import tabulate
import re
import struct
import sys
import coloredlogs
import logging
import fcntl
import termios
import os
import yaml
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit import prompt




with open('libs/templates/var.json','r') as f :
    var_json = json.load(f)


def check_existence(endpoint,var):
    from libs.auth import get_headers
    url = get_url(endpoint)
    key = var_json['key'][endpoint]
    headers = get_headers()
    headers = headers['data']
    try :
        result = requests.get(url, headers=headers )
        result = result.json()
        msg = result['message']
        result = result['data']
    except Exception as e:
        respons = generate_respons(False,str(e))
    if result is None:
        if 'Invalid access token' in msg:
            respons = generate_respons(False,'Your token has expired')
        else : respons = generate_respons(False, "No DNS")
    else :   
        for i in result:
            if i[key] == var:
                respons = generate_respons(True,'Value already exist',i[key])
                break
            else :
                respons = generate_respons(False,'Value doesnt exist')
    return respons

def get_url(endpoint):
    url = "http://103.89.5.121:6968/api/"
    #url = "http://127.0.0.1:6968/api/"

    url = url + var_json['endpoints'][endpoint]

    return url

def get_idkey(endpoint,headers):

    url = get_url(endpoint)
    res = requests.get(url)
    data = res.json()
    data = data['data']
    idname = var_json['id'][endpoint]
       
    return idname




def get_time():
    now = datetime.datetime.now()
    res = now.strftime("%Y%m%d%H")
    return res


def log_err(stdin): #pragma: no cover
    coloredlogs.install()
    logging.error(stdin)    

def log_warning(stdin): #pragma: no cover
    coloredlogs.install()
    logging.warning(stdin)

def assurance(): #pragma: no cover
    catch = input("Are you sure ? (Y/N)")
    catch = catch.upper()
    if catch == 'Y' or catch == 'YES':
        return True
    else :
        return False

def dictcleanup(obj): #pragma: no cover 
    result = dict()
    keys = obj.keys()
    for key in keys:
        temp = key.encode('utf-8')
        result[temp] = obj[key].encode('utf-8')

    return result

def listcleanup(obj): #pragma: no cover 
    for row in obj:
        row = row.encode('utf-8')
    return row

# def get_table_head(row):
#     keys = row.keys()
#     return keys

def check_availability(obj,length):
    for i in obj:
        try:
            if int(i) > length or int(i) < 0:
                print("index {} is invalid integer and will be ignored".format(i))
                obj.remove(i)
            elif i ==',':
                pass
            elif type(i) != int:
                #print("invalid input")
                pass
        except Exception as e:
            #print(str(e))
            sys.stderr.write(str(e))
    return obj

def table_cleanup(obj):
    obj = convert(obj)
    keys = list(obj[0].keys())
    temp = list()
    for key in keys:
        if 'id' in key:
            temp.append(key)
    for row in obj:
        for key in temp:
            del row[key]
    return obj
        
def get_filter(obj):
    var = {
    "--nm-record" : "nm_record",
    "--nm-zone"   : "nm_zone",
    "--type"      : "nm_type",
    "--ttl"       : "nm_ttl"
    }
    keys = obj.keys()
    result = dict()

    
    for key in keys:
        if key in var.keys() and obj[key] is not None:
            if key == '--ttl' or key == '--type':
                check=check_existence(key.strip('-'),obj[key])
                if not check['status'] : continue
            result[var[key]] = obj[key]
    return result


def convert(data):
  if isinstance(data, bytes):      return data.decode()
  if isinstance(data, (str, int)): return str(data)
  if isinstance(data, dict):       return dict(map(convert, data.items()))
  if isinstance(data, tuple):      return tuple(map(convert, data))
  if isinstance(data, list):       return list(map(convert, data))
  if isinstance(data, set):        return set(map(convert, data))

def generate_respons(status,message,data=None):
    if data : return {"status" : status, "data" : data, "message": message}
    else : return {"status": status, "message" : message}

 