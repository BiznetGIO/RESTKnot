import pytest
import json
import utils
from utils import post_data

class Vars:
    ids = dict()



class TestZone:
    
    var_mock = Vars()

    def post_data(self,client,endpoint,data,headers):
        url = 'api/'+endpoint
        res = client.post(url,data=json.dumps(data),
                    content_type='application/json', headers=headers)
        return res

    @pytest.mark.run(order=1)
    def test_get_zone(self,client,get_header,get_mock):
    
        header = get_header
        result = client.get('api/zone',headers=header)
        assert result.status_code == 200


        ## Check without authorization
        header = {"Access-Token" : "aa"}
        result = client.get('api/zone',headers=header)
        assert result.status_code == 200

        ## INSERT ZONE

        nm_zone = get_mock['nm_zone']
        header = get_header
        
        data = utils.get_model('add',{"nm_zone" : nm_zone})
        result = self.post_data(client,'zone',data=data, headers=header)

        assert result.status_code == 200

        ## Failure
        data = utils.get_model('add',{"nm_zone" : 123})
        result = self.post_data(client,'zone',data=data, headers=header)
        assert result.status_code == 200


        ## Search Zone

        nm_zone = get_mock['nm_zone']
        header = get_header

        data = utils.get_model('where',{"nm_zone" : nm_zone})
        result = self.post_data(client,'zone',data=data, headers=header)
        assert result.status_code == 200

        result = json.loads(result.data.decode('utf8'))
        self.var_mock.ids['id_zone'] = result['data'][0]['id_zone']

        data = utils.get_model('where',{"nm_zone" : list()})
        result = self.post_data(client,'zone',data=data, headers=header)

        assert result.status_code == 200

        ## SYNC_ZONE

        headers = get_header
        id_zone = self.var_mock.ids['id_zone']
        data = {'conf-insert': {'tags': {'id_zone': id_zone}}}
        result = self.post_data(client,'sendcommand',data=data, headers=headers)
        assert result.status_code == 200

        ## Check Sync

        data = {'zone-read': {'tags': {'id_zone': id_zone}}}
        result = self.post_data(client,'sendcommand',data=data, headers=headers)
        assert result.status_code == 200

        # GET TTL
        headers = get_header
        nm_ttl = get_mock['nm_ttl']
        data = utils.get_model('where',{"nm_ttl" : nm_ttl})
        result = self.post_data(client,'ttl',data=data, headers=headers)
        assert result.status_code == 200

        result = json.loads(result.data.decode('utf8'))
        id_ttl = result['data'][0]['id_ttl']
        self.var_mock.ids['id_ttl'] = id_ttl

        # GET TYPE

        header = get_header
        nm_type = get_mock['nm_type']
        data = utils.get_model('where',{"nm_type" : nm_type})
        result = self.post_data(client,'type',data=data, headers=header)
        assert result.status_code == 200

        result = json.loads(result.data.decode('utf8'))
        id_type = result['data'][0]['id_type']
        self.var_mock.ids['id_type'] = id_type

        data = utils.get_model('where',{"nm_type" : "NS"})
        result = self.post_data(client,'type',data=data, headers=header)
        result = json.loads(result.data.decode('utf8'))
        id_type = result['data'][0]['id_type']
        self.var_mock.ids['id_type_1'] = id_type




        ## ADD RECORD
        header = get_header
        id_zone = self.var_mock.ids['id_zone']
        id_type = self.var_mock.ids['id_type']
        data = utils.get_model('add',{"nm_record" : "soatest", "date_record" : "2018090909",
                                "id_zone" : str(id_zone), "id_type" : str(id_type)})
        
        result = self.post_data(client,'record',data=data, headers=header)
        print("CC : ",result.data)
        assert result.status_code == 200

        result = json.loads(result.data.decode('utf8'))
        id_record = result["message"]["id"]
        self.var_mock.ids['id_record'] = id_record

        ### ADD NS

        id_type = self.var_mock.ids['id_type_1']
        data = utils.get_model('add',{"nm_record" : "nstest", "date_record" : "2018090909",
                                "id_zone" : str(id_zone), "id_type" : str(id_type)})
        
        result = self.post_data(client,'record',data=data, headers=header)
        assert result.status_code == 200

        result = json.loads(result.data.decode('utf8'))
        id_record = result["message"]["id"]
        self.var_mock.ids['id_record_ns'] = id_record




        ## ADD TTL_DATA
        header = get_header
        id_record = self.var_mock.ids['id_record']
        id_ttl = self.var_mock.ids['id_ttl']

        data = utils.get_model('add',{"id_record" : id_record , "id_ttl" : id_ttl})

        result = self.post_data(client,'ttldata',data=data, headers=header)
        assert result.status_code == 200

        result = json.loads(result.data.decode('utf8'))
        self.var_mock.ids['id_ttldata'] = result['message']['id']

        ## ADD NS TTLDATA
        id_record = self.var_mock.ids['id_record_ns']
        data = utils.get_model('add',{"id_record" : id_record , "id_ttl" : id_ttl})
        result = self.post_data(client,'ttldata',data=data, headers=header)
        result = json.loads(result.data.decode('utf8'))
        self.var_mock.ids['id_ttldata_ns'] = result['message']['id']



        # ADD CONTENT
        id_ttldata = self.var_mock.ids['id_ttldata']
        header = get_header

        data = utils.get_model('add',{"id_ttldata" : id_ttldata, "nm_content" : "soacontent"})
        result = self.post_data(client,'content',data=data, headers=header)
        assert result.status_code == 200
        result = json.loads(result.data.decode('utf-8'))
        id_content = result['message']['id']
        self.var_mock.ids['id_content']=id_content

        ## ADD CONTENT NS

        id_ttldata = self.var_mock.ids['id_ttldata_ns']

        data = utils.get_model('add',{"id_ttldata" : id_ttldata, "nm_content" : "ns"})
        result = self.post_data(client,'content',data=data, headers=header)
        result = json.loads(result.data.decode('utf-8'))
        id_content = result['message']['id']
        self.var_mock.ids['id_content_ns']=id_content

        ## ADD CONTENT SERIAL
        id_record = self.var_mock.ids['id_record']
        header = get_header
        content_serial = 'test_content_serial'

        data = utils.get_model('add',{"id_record" : id_record, "nm_content_serial" : content_serial})
        result = self.post_data(client,'content_serial',data=data, headers=header)
        
        assert result.status_code == 200
        
        result = json.loads(result.data.decode('utf-8'))
        id_content_serial = result['message']['id']
        self.var_mock.ids['id_content_serial'] = id_content_serial


     ##SYNCHRONIZATION


    ## SOA
        headers = get_header
        id_zone = self.var_mock.ids['id_zone']
        data = {'zone-soa-insert': {'tags': {'id_zone': id_zone}}}
        res = self.post_data(client,'sendcommand',data,headers)
        assert res.status_code == 200

    ## NS
        data = {'zone-ns-insert': {'tags': {'id_zone': id_zone}}}
        res = self.post_data(client,'sendcommand',data,headers)
        assert res.status_code == 200

    ### Start record Removal, Unsync Record First
        id_record = self.var_mock.ids['id_record']
        data = {"zone-unset":{"tags":{"id_record" : id_record}}}
        data_test = {"where":{"tags":{"id_record": id_record}}}
        res_test = self.post_data(client,'record',data_test,headers)
        res_json = json.loads(res_test.data.decode('utf8'))
        print(res_json)
        res = self.post_data(client,'sendcommand',data,headers)
        
        assert res.status_code == 200

        id_record = self.var_mock.ids['id_record_ns']
        data = {"zone-unset":{"tags":{"id_record" : id_record}}}
        res = self.post_data(client,'sendcommand',data,headers)

        ## REMOVE CONTENT SERIAL

        id_content_serial = self.var_mock.ids['id_content_serial']
        data = utils.get_model("remove",{"id_content_serial" : id_content_serial})
        res = self.post_data(client,'content_serial',data,get_header)
        assert res.status_code == 200

        ## REMOVE CONTENT
        id_content = self.var_mock.ids['id_content']
        data = utils.get_model("remove",{"id_content" : id_content})
        res = self.post_data(client,'content',data,get_header)
        assert res.status_code == 200

        ## REMOVE TTL DATA
        id_ttldata = self.var_mock.ids['id_ttldata']
        data = utils.get_model("remove",{"id_ttldata" : id_ttldata})
        res = self.post_data(client,'ttldata',data,get_header)
        assert res.status_code == 200
        
        ## REMOVE RECORD
        id_record = self.var_mock.ids['id_record']
        data = utils.get_model("remove",{"id_record" : id_record})
        res = self.post_data(client,'record',data,get_header)
        assert res.status_code == 200

        ## REMOVE ZONE
        id_zone = self.var_mock.ids['id_zone']
        header = get_header

        data = {"conf-unset":{"tags":{"id_zone" : id_zone}}}
        result = self.post_data(client,'sendcommand',data,header)
        assert result.status_code == 200

        data = utils.get_model('remove', {"id_zone" : id_zone})
        result = self.post_data(client,'zone',data=data, headers=header)
        assert result.status_code == 200



    def test_query(self,client,get_header):
        jsonq = {
                    "query": {
                        "select": {
                            "fields": "nm_zone",
                            "where": {
                                "column" : "nm_zone",
                                "value" : "ikan.com"
                                },
                            "join": ""
                            }
                        }
                    }
                
                
                
        queer = client.post('api/zone',
                data = json.dumps(jsonq),
                content_type = 'application/json',
                headers = get_header)
        assert queer.status_code == 200

    def test_query_list(self,client,get_header):
        jsonq = {
                    "query": {
                        "select": {
                            "fields": ["nm_zone",'nm_type'],
                            "where": {
                                "column" : "nm_zone",
                                "value" : "ikan.com"
                                },
                            "join": ""
                            }
                        }
                    }
                
                
                
        queer = client.post('api/zone',
                data = json.dumps(jsonq),
                content_type = 'application/json',
                headers = get_header)
        assert queer.status_code == 200

    def test_query_empty(self,client,get_header):
        jsonq = {
                    "query": {
                        "select": {
                            "fields": "nm_zone",
                            "where": "",
                            "join": ""
                            }
                        }
                    }
                
                
                
        queer = client.post('api/zone',
                data = json.dumps(jsonq),
                content_type = 'application/json',
                headers = get_header)
        assert queer.status_code == 200

    def test_query_insert(self,client,get_header):
        jsonq = {
            "query":{
                "insert": {
                    "column": {
                        "name": "nm_zone",
                    },
                    "values": {
                        "name": "monkey.com",
                    },
                    "return":  "id_zone"
                        
                    }
                }
            }
                
                
                
        queer = client.post('api/zone',
                data = json.dumps(jsonq),
                content_type = 'application/json',
                headers = get_header)
        assert queer.status_code == 200

    def test_query_insert_empty(self,client,get_header):
        jsonq = {
            "query":{
                "insert": {
                    "column": {
                        "name": "",
                    },
                    "values": {
                        "name": "",
                    },
                    "return":  ""
                        
                    }
                }
            }
                
                
        queer = client.post('api/zone',
                data = json.dumps(jsonq),
                content_type = 'application/json',
                headers = get_header)
        assert queer.status_code == 200

    def test_query_insert_list(self,client,get_header):
        jsonq = {
            "query":{
                "insert": {
                    "column": {
                        "name": ["nm_zone","nm_type"],
                    },
                    "values": {
                        "nm_zone": "monkey.com",
                        "nm_type":"SRV"
                    },
                    "return":  ["id_zone","id_type"]
                        
                    }
                }
            }
                
                
                
        queer = client.post('api/zone',
                data = json.dumps(jsonq),
                content_type = 'application/json',
                headers = get_header)
        assert queer.status_code == 200

    @pytest.mark.run(order=16)
    def test_userzone(self,client,get_header,generate_userdata,get_creds):
        user_id = get_creds['user_id']
        header = get_header
        header['user-id'] = '9c2ebe8a3664b8cc847b3c61c78c30ba471d87c9110dfb25bbe9250b9aa46e91'
        data = {"id_zone" : self.var_mock.ids['id_zone']}
        res = self.post_data(client,'userzone',data=data,headers=header)
        assert res.status_code == 200
        res = client.get('api/userzone',headers=header)
        assert res.status_code == 200
        
        
