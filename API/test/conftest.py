import pytest
from app import create_app,db
import requests
import json
import test
from test.utils import *


headers = dict()
expirehead = dict()
data_id = dict()
zone_id = ''

@pytest.fixture
def app():
    app = create_app()
    return app

@pytest.fixture(scope = 'session', autouse=True)
def a_tokenTest():
    response=requests.request("POST",url='http://127.0.0.1:6968/api/sign', data={'username': 'ikan', 'password': 'fish'})
    result = response.json()
    tokensession=result['data']['apikey']
    #refreshtoken=result['data']['refresh']
    global headers
    headers = { 
        'access_token':
                {
            'Authorization' : str(tokensession)
             }
             #,
        # 'refresh_token':
        # {
        #     'Authorization' : str(refreshtoken)
        # }
        }
    return headers

@pytest.fixture(scope = 'module', autouse=True)
def a_expiredToken():
    response=requests.request("POST",url='http://127.0.0.1:6968/api/sign', data={'username': 'testtoken', 'password': '1234'})
    result = response.json()
    extokensession=result['data']['apikey']
    global expirehead
    expirehead = {
            'Authorization' : str(extokensession)
        }
    return expirehead

@pytest.fixture
def extokentest():
    return expirehead

@pytest.fixture(autouse=True)
def tokentest():
    return headers['access_token']

# @pytest.fixture(autouse=True)
# def refreshtokentest():
#     return headers['refresh_token']
    

@pytest.fixture(autouse=True,scope = 'session')
def a_zone_check():
    #Check the table zone, if it's empty ==> insert one data
    token = headers['access_token']
    zone_list = list()
    id_list = list()
    res = requests.request("GET",url='http://127.0.0.1:6968/api/zone',headers = token)
    data = res.json()
    global zone_id
    for i in data['data']:
        zone_list.append(i['nm_zone'])
        if(i['nm_zone']=='test.com'):
            zone_id = i['id_zone']
            #return(i['id_zone'])
    if not 'test.com' in zone_list:
        testdata = {
            'domain' : 'test.com'
        }
        res = requests.request("POST",
                            url='http://127.0.0.1:6968/api/user/dnscreate', 
                            data = testdata,
                            headers = token )
        data = res.json()
        zone_id = data['data']['data']['id_zone']
        #return data['data']['data']['id_zone']
    return zone_id


@pytest.fixture(autouse=True,scope='session')
def b_checkfundamentals():
    token = headers['access_token']
    temp = list()
    ttl_list = ['86400','43200','28800','14400','7200','3600','1800','900','300']
    type_list = ['SOA','SRV','A','NS','CNAME','MS','AAAA','TXT']
    url = 'http://127.0.0.1:6968/api/'
    fieldname = ''
    val = ''
    data_send = {"insert": {"fields": { fieldname : val }}}
    res = requests.request("GET", url=url+'ttl',headers = token)
    data = res.json()
    for i in data['data']:
        temp.append(i['nm_ttl'])
    for i in ttl_list :
        if not i in temp:
            fieldname = 'nm_ttl'
            val = i
            res = requests.post(url=url+'ttl',
                                data = json.dumps(data_send),
                                headers = token)
        else :
            print(i," ada \n")

    res = requests.request("GET", url=url+'type',headers = token)
    data = res.json()
    for i in data['data']:
        temp.append(i['nm_type'])
    for i in type_list :
        if not i in temp:
            fieldname = 'nm_type'
            val = i
            res = requests.post(url=url+'type',
                                data = json.dumps(data_send),
                                headers = token)
        else :
            print(i," ada \n")

@pytest.fixture(autouse=True,scope='session')   
def grabIds():
    global data_id
    checkzone = zone_id
    tokentest = headers['access_token']
    data_id = dict()
    data_id['record']=list()
    data_id['ttldata'] = list()
    data_id['content'] = list()
    data_id['content_serial'] = list()
    record_view = {"view": {"tags": {"id_record": ""}}}
    res = requests.post(url='http://127.0.0.1:6968/api/record',
                        data = json.dumps(record_view),
                        headers = tokentest)
    data = res.json()
    temp = dict()
    for i in data['data']:
        temp=i
        temp['id_zone']=getId(i['nm_zone'],'zone',tokentest)
        temp['id_type']=getId(i['nm_type'],'type',tokentest)
        temp.pop('nm_record',None)
        temp.pop('nm_zone',None)
        temp.pop('nm_type',None)
        if(i['id_zone']==checkzone):
            data_id['record'].append(temp)
    
    ttldata_view = {"view": {"tags": {"id_ttldata": ""}}}
    res = requests.post(url='http://127.0.0.1:6968/api/ttldata',
                        data = json.dumps(ttldata_view),
                        headers = tokentest)
    data = res.json()
    temp = dict()
    for i in data['data']:
        temp=i
        temp['id_record']=getId(i['nm_record'],'record',tokentest)
        temp['id_zone']=getId(i['nm_zone'],'zone',tokentest)        
        temp.pop('nm_ttl',None)
        temp.pop('nm_zone',None)
        temp.pop('nm_record',None)
        if(i['id_zone']==checkzone):
            data_id['ttldata'].append(temp)

    contentdata_view = {"view": {"tags": {"id_content": ""}}}
    res = requests.post(url='http://127.0.0.1:6968/api/content',
                        data = json.dumps(contentdata_view),
                        headers = tokentest)
    data = res.json()
    temp = dict()
    for i in data['data']:
        temp=i
        temp['id_record']=getId(i['nm_record'],'record',tokentest)
        temp['id_zone']=getId(i['nm_zone'],'zone',tokentest) 
        temp['id_type']=getId(i['nm_type'],'type',tokentest)
        temp['id_ttl']=getId(i['nm_ttl'],'ttl',tokentest)       
        temp.pop('nm_ttl',None)
        temp.pop('nm_zone',None)
        temp.pop('nm_record',None)
        temp.pop('nm_content',None)
        temp.pop('nm_type',None)
        if(i['id_zone']==checkzone):
            data_id['content'].append(temp)

    contentser_view = {"view": {"tags": {"id_content_serial": ""}}}
    res = requests.post(url='http://127.0.0.1:6968/api/content_serial',
                        data = json.dumps(contentser_view),
                        headers = tokentest)
    data = res.json()
    temp = dict()
    for i in data['data']:
        temp=i
        temp['id_record']=getId(i['nm_record'],'record',tokentest)
        temp['id_zone']=getId(i['nm_zone'],'zone',tokentest) 
        temp['id_type']=getId(i['nm_type'],'type',tokentest)
        temp.pop('nm_zone',None)
        temp.pop('nm_record',None)
        temp.pop('nm_content_serial',None)
        temp.pop('nm_type',None)
        if(i['id_zone']==checkzone):
            data_id['content_serial'].append(temp)
            
    return data_id

@pytest.fixture(autouse=True)
def z_idtest():
    return zone_id

@pytest.fixture(autouse=True)
def z_datatest():
    #print(data_id)
    return data_id

@pytest.fixture(scope='class',autouse=True)
def z_prep_var_command_srv():
    token = headers['access_token']
    query = "select * from v_record where id_zone ='"+zone_id+"' AND nm_type = 'SRV'"
    db.execute(query)
    rows = db.fetchall()
    if not rows:
        type_id = getId('SRV','type',token)
        data_record = {
                "insert": {
                    "fields": {
                        "nm_record":"ThisIsaTest",
                        "date_record":"2018070410",
                        "id_zone":zone_id,
                        "id_type":type_id
                        }     
                    }
                }
        res_record = requests.post(url='http://127.0.0.1:6968/api/record',
                        data = json.dumps(data_record),
                        headers = token)
        temp = res_record.json()
        print(temp)
        record_id = temp['message']['id']
        print(record_id)
        ttl_id = getId('14400','ttl',token)
        
        data_ttldata = {
                "insert": {
                    "fields": {
                        "id_record": record_id,
                        "id_ttl": ttl_id
                        }     
                    }
                }
        res_ttldata = requests.post(url='http://127.0.0.1:6968/api/ttldata',
                        data = json.dumps(data_ttldata),
                        headers = token)
        temp = res_ttldata.json()
        ttldata_id = temp['message']['id']
        
        data_content = {
                "insert": {
                    "fields": {
                        "id_ttldata": ttldata_id,
                        "nm_content": 'This is a test'
                        }     
                    }
                }
        res_content = requests.post(url='http://127.0.0.1:6968/api/content',
                        data = json.dumps(data_content),
                        headers = token)
        
        data_cs = {
                "insert": {
                    "fields": {
                        "nm_content_serial": '38400',
                        "id_record": record_id
                        }     
                    }
                }
        res_cs = requests.post(url='http://127.0.0.1:6968/api/content_serial',
                        data = json.dumps(data_cs),
                        headers = token)

    return zone_id

@pytest.fixture(scope='class',autouse = True)
def z_prep_var_command_mx():
    token = headers['access_token']
    query = "select * from v_record where id_zone ='"+zone_id+"' AND nm_type = 'MX'"
    db.execute(query)
    rows = db.fetchall()
    if not rows:
        type_id = getId('MX','type',token)
        data = {
                "insert": {
                    "fields": {
                        "nm_record":"ThisIsaTest",
                        "date_record":"2018070410",
                        "id_zone":zone_id,
                        "id_type":type_id
                        }     
                    }
                }
        res = requests.post(url='http://127.0.0.1:6968/api/record',
                        data = json.dumps(data),
                        headers = token)
        temp = res.json()
        print(temp)
        record_id = temp['message']['id']
        print(record_id)
        ttl_id = getId('14400','ttl',token)
        
        data_ttldata = {
                "insert": {
                    "fields": {
                        "id_record": record_id,
                        "id_ttl": ttl_id
                        }     
                    }
                }
        res_ttldata = requests.post(url='http://127.0.0.1:6968/api/ttldata',
                        data = json.dumps(data_ttldata),
                        headers = token)
        temp = res_ttldata.json()
        ttldata_id = temp['message']['id']
        
        data_content = {
                "insert": {
                    "fields": {
                        "id_ttldata": ttldata_id,
                        "nm_content": 'This is a test'
                        }     
                    }
                }
        res_content = requests.post(url='http://127.0.0.1:6968/api/content',
                        data = json.dumps(data_content),
                        headers = token)
        
        data_cs = {
                "insert": {
                    "fields": {
                        "nm_content_serial": '38400',
                        "id_record": record_id
                        }     
                    }
                }
        res_cs = requests.post(url='http://127.0.0.1:6968/api/content_serial',
                        data = json.dumps(data_cs),
                        headers = token)
    return zone_id