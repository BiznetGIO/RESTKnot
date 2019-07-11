import pytest
import json
import utils

class Vars:
    ids = dict()

class DataTest(object):
    identity = None
    record_type = {
        "soa" : "402140280385142785",
        "srv" : "402329131320508417",
        "a"   : "402386688803307521",
        "ns"  : "402393625286410241",
        "cname": "402427533112147969",
        "mx"  : "402427545745850369",
        "aaaa": "402427683852124161",
        "txt" : "402427759247851521"
    }

    def post_data(self,client,endpoint,data,headers):
        url = 'api/'+endpoint
        res = client.post(url,data=json.dumps(data),
        content_type='application/json', headers=headers)
        return res

    def generate_empty_data(self):
        self.identity = {
            "zone": None,
            "records": list(),
            "content": list(),
            "content_serial": list()
        }
        

    def add_zone(self,client,nm_zone,headers):
        dataset = {}
        url = 'user/dnscreate'
        data = {"domain": nm_zone}
        res = self.post_data(client,url,data,headers)
        tmp = json.loads(res.data.decode('utf8'))
        if str(tmp['code']) == '200':
            dataset['id_zone'] = tmp['data']['data']['id_zone']
            dataset['nm_zone'] = tmp['data']['data']['nm_zone']
        elif str(tmp['code']) == '401':
            where = {"nm_zone": nm_zone}
            where = utils.get_model('where',where)
            res = self.post_data(client,'zone',where,headers)
            data = json.loads(res.data.decode('utf8'))
            data = data['data'][0]
            dataset['id_zone'] = data['id_zone']
            dataset['nm_zone'] = nm_zone
        if not self.identity:
            self.generate_empty_data()
        self.identity['zone'] = dataset
        return res
    
    def add_record(self,client,nm_record,type_,headers):
        url = 'record'
        id_type = self.record_type[type_.lower()]
        data = {"id_zone": self.identity['zone']['id_zone'], "nm_record": nm_record, "id_type": id_type, "date_record": "2019220207"}
        send_data = utils.get_model("add",data)
        res = self.post_data(client,url,send_data,headers)
        id_record = json.loads(res.data.decode('utf8'))
        try:
            id_record = id_record['message']['id']
        except Exception:
            print(json.loads(res.data.decode('utf8')))
        if not self.identity:
            self.identity['records'].append(id_record)        
        return res

    def add_content_data(self,client,content,id_record,headers):
        dataset = dict()
        endpoint = 'ttldata'
        data = {"id_record" : id_record, "id_ttl": "402428126292705281"}
        json_send = utils.get_model("add",data)
        res = self.post_data(client,endpoint,json_send,headers)
        tmp = json.loads(res.data.decode('utf8'))
        id_ttldata = tmp['message']['id']

        endpoint = 'content'
        data = {"id_ttldata": id_ttldata, "nm_content": content}
        json_send= utils.get_model("add",data)
        res = self.post_data(client,endpoint,json_send,headers)
        tmp = json.loads(res.data.decode('utf8'))
        
        id_content = tmp['message']['id']

        dataset['id_ttldata'] = id_ttldata
        dataset['id_content'] = id_content
        dataset['id_record'] = id_record

        try:
            self.identity['content'].append(dataset)
        except Exception:
            if not self.generate_empty_data:
                self.generate_empty_data()
                self.identity['content'].append(dataset)
        return dataset

    def add_content_serial(self,client,content_serial,id_record,headers):
        dataset = dict()
        endpoint = 'content_serial'
        data = {"id_record" : id_record, "nm_content_serial": content_serial}
        json_send = utils.get_model('add',data)
        res = self.post_data(client,endpoint,json_send,headers)
        tmp = json.loads(res.data.decode('utf8'))
        id_content_serial = tmp['message']['id']
        dataset['id_content_serial'] = id_content_serial
        dataset['id_record'] = id_record
        try:
            self.identity['content_serial'].append(dataset)
        except Exception:
            if not self.identity:
                self.generate_empty_data()
                self.identity['content_serial'].append(dataset)        
        return dataset

    def add_error_record(self,client,nm_record,type_,headers):
        url = 'record'
        id_type = self.record_type[type_.lower()]
        data = {"id_zone": self.identity['zone']['id_zone'], "nm_record": nm_record, "id_type": id_type, "date_record": "2019220207"}
        send_data = utils.get_model("add",data)
        res = self.post_data(client,url,send_data,headers)
        return res

    def edit_content_data(self,client,id_content,id_record,new_content,headers):
        fields = {"fields": {"nm_content": new_content}}
        tags = {"tags":{"id_content": id_content}}
        send_data = {"edit": {**fields, **tags}}
        res = self.post_data(client,'content',send_data,headers)
        data = {"zone-insert": {"tags":{"id_record": id_record}}}
        res = self.post_data(client,'sendcommand',data,headers)
        return res

    def edit_ttldata(self,client,id_ttldata,new_ttl,id_record,headers):
        fields = {"fields": {"id_ttl": new_ttl,"id_record": id_record}}
        tags = {"tags": {"id_ttldata": id_ttldata}}
        send_data = {"edit": {**fields, **tags}}
        res = self.post_data(client,'ttldata',send_data,headers)
        data = {"zone-insert": {"tags":{"id_record": id_record}}}
        res = self.post_data(client,'sendcommand',data,headers)
        return res

    def edit_record(self,client,id_record,new_data,headers):
        fields = {
            "nm_record": new_data["nm_record"],
            "date_record": new_data["date_record"],
            "id_zone": new_data["id_zone"],
            "id_type": new_data["id_type"]
        }
        fields = {"fields" : fields}
        tags = {"tags": {"id_record": id_record}}
        send_data = {"edit": {**fields, **tags}}
        res = self.post_data(client,'record',send_data,headers)
        data = {"zone-insert": {"tags":{"id_record": id_record}}}
        res = self.post_data(client,'sendcommand',data,headers)
        return res

    def edit_serial_data(self,client,headers,id_content_serial,id_record,new_content_serial):
        fields = { "nm_content_serial": new_content_serial}
        fields = {"fields" : fields}
        tags = {"tags": {"id_content_serial": id_content_serial}}
        send_data = {"edit": {**fields, **tags}}
        res = self.post_data(client,'content_serial',send_data,headers)
        data = {"zone-insert": {"tags":{"id_record": id_record}}}
        res = self.post_data(client,'sendcommand',data,headers)
        return res



    def teardown(self,client,headers):
        id_zone = self.identity['zone']['id_zone']
        id_records = self.identity['records']
        for i in id_records:
            data = {"zone-unset":{"tags":{"id_record" : id_record}}}
            self.post_data(client,'sendcommand',data,headers)

        data = {"conf-unset":{"tags":{"id_zone" : id_zone}}}
        self.post_data(client,'sendcommand',data,headers)
        
        data = {'id_zone': id_zone}
        send_data = utils.get_model('remove',data)
        self.post_data(client,'zone',send_data,headers)

    def add_content_data_fail(self,client,content,id_record,headers):
        dataset = dict()
        endpoint = 'ttldata'
        data = {"id_record" : id_record, "id_ttl": "402428126292705281"}
        json_send = utils.get_model("add",data)
        res = self.post_data(client,endpoint,json_send,headers)
        tmp = json.loads(res.data.decode('utf8'))
        id_ttldata = tmp['message']['id']

        endpoint = 'content'
        data = {"id_ttldata": id_ttldata, "nm_content": content}
        json_send= utils.get_model("add",data)
        res = self.post_data(client,endpoint,json_send,headers)
        tmp = json.loads(res.data.decode('utf8'))
        print(tmp)
        assert tmp['status'] == 'error'


    def add_content_serial_fail(self,client,content_serial,id_record,headers):
        endpoint = 'content_serial'
        data = {"id_record": id_record,"nm_content_serial":content_serial}
        json_send = utils.get_model("add",data)
        res = self.post_data(client,endpoint,json_send,headers)
        tmp = json.loads(res.data.decode('utf8'))
        assert tmp['status'] == 'error'

    def teardown_record(self,client,id_record,headers):
        data = {"zone-unset":{"tags":{"id_record" : id_record}}}
        self.post_data(client,'sendcommand',data,headers)
        data = {"id_record": id_record}
        data = utils.get_model("remove",data)
        self.post_data(client,'record',data,headers)

class TestValidation:


    testset = list()

    def post_data(self,client,endpoint,data,headers):
        url = 'api/'+endpoint
        res = client.post(url,data=json.dumps(data),
        content_type='application/json', headers=headers)
        return res

    def assert_hostname(self,respons,expected,zone):
        result = json.loads(respons.data.decode('utf8'))
        result = result['data']['data']
        print(result)
        zn_knot = zone+"."
        hostnames = list(result[zn_knot].keys())
        assert expected in hostnames
        return result[zn_knot][expected]

    def assert_error(self,respons,expected,zone):
        result = json.loads(respons.data.decode('utf8'))

    def assert_value(self,respons,expected,record_type):
        data = respons[record_type.upper()]
        data = data['data']
        assert expected in data

    def test_validation_hostname(self,client,get_header):
        ####################### CNAME ######################

        record_type = 'cname'

        headers = get_header
        test_data = DataTest()
        self.testset.append(test_data)
        res = test_data.add_zone(client,"wetestzone.xyz",headers)
        assert res.status_code == 200
        
        ########## hostname : @ , content: wetestzone.xyz
        res = test_data.add_record(client,"@",record_type,headers)
        assert res.status_code == 200
        res = json.loads(res.data.decode('utf8'))
        id_record = res['message']['id']
        res = test_data.add_content_data(client,'wetestzone.xyz',id_record,headers)

        data = {"zone-insert": {"tags":{"id_record": id_record}}}
        res = test_data.post_data(client,'sendcommand',data,headers)
        res = json.loads(res.data.decode('utf8'))
        
        # ZONE READ
        id_zone = test_data.identity['zone']['id_zone']
        data = {"zone-read" : {"tags":{"id_zone": id_zone}}}
        res = test_data.post_data(client,'sendcommand',data,headers)
        nm_zone = test_data.identity['zone']['nm_zone']
        respons = self.assert_hostname(res,'wetestzone.xyz.',nm_zone)
        self.assert_value(respons,'wetestzone.xyz.wetestzone.xyz.',record_type)
        test_data.teardown_record(client,id_record,headers)

        ############## hostname : wetestzone.xyz , content : wetestzone.xyz.    
        
        res = test_data.add_record(client,"wetestzone.xyz",record_type,headers)
        assert res.status_code == 200
        res = json.loads(res.data.decode('utf8'))
        id_record = res['message']['id']
        res = test_data.add_content_data(client,'wetestzone.xyz.',id_record,headers)

        data = {"zone-insert": {"tags":{"id_record": id_record}}}
        res = test_data.post_data(client,'sendcommand',data,headers)
        res = json.loads(res.data.decode('utf8'))
        
        # ZONE READ
        id_zone = test_data.identity['zone']['id_zone']
        data = {"zone-read" : {"tags":{"id_zone": id_zone}}}
        res = test_data.post_data(client,'sendcommand',data,headers)
        nm_zone = test_data.identity['zone']['nm_zone']
        res=self.assert_hostname(res,'wetestzone.xyz.wetestzone.xyz.',nm_zone)
        self.assert_value(res,'wetestzone.xyz.',record_type)
        data = {"zone-unset":{"tags":{"id_record" : id_record}}}
        self.post_data(client,'sendcommand',data,headers)
        data = {"id_record": id_record}
        data = utils.get_model("remove",data)
        res=self.post_data(client,'record',data,headers)
        test_data.teardown_record(client,id_record,headers)
        # ##### hostname : www , content: @

        # res = test_data.add_record(client,"www",record_type,headers)
        # assert res.status_code == 200
        # res = json.loads(res.data.decode('utf8'))
        # id_record = res['message']['id']
        # res = test_data.add_content_data(client,'@',id_record,headers)

        # data = {"zone-insert": {"tags":{"id_record": id_record}}}
        # res = test_data.post_data(client,'sendcommand',data,headers)
        # res = json.loads(res.data.decode('utf8'))
        
        # # ZONE READ
        # id_zone = test_data.identity['zone']['id_zone']
        # data = {"zone-read" : {"tags":{"id_zone": id_zone}}}
        # res = test_data.post_data(client,'sendcommand',data,headers)
        # nm_zone = test_data.identity['zone']['nm_zone']
        # res=self.assert_hostname(res,'www.wetestzone.xyz.',nm_zone)
        # self.assert_value(res,'wetestzone.xyz.',record_type)
        # test_data.teardown_record(client,id_record,headers)

        ##### hostname : a.b.c  content: mail.google.com

        res = test_data.add_record(client,"a.b.c",record_type,headers)
        assert res.status_code == 200
        res = json.loads(res.data.decode('utf8'))
        id_record = res['message']['id']
        res = test_data.add_content_data(client,'mail.google.com',id_record,headers)

        data = {"zone-insert": {"tags":{"id_record": id_record}}}
        res = test_data.post_data(client,'sendcommand',data,headers)
        res = json.loads(res.data.decode('utf8'))
        
        # ZONE READ
        id_zone = test_data.identity['zone']['id_zone']
        data = {"zone-read" : {"tags":{"id_zone": id_zone}}}
        res = test_data.post_data(client,'sendcommand',data,headers)
        nm_zone = test_data.identity['zone']['nm_zone']
        res=self.assert_hostname(res,'a.b.c.wetestzone.xyz.',nm_zone)
        self.assert_value(res,'mail.google.com.wetestzone.xyz.',record_type)
        test_data.teardown_record(client,id_record,headers)

        ##### hostname : a.b.c  content: mail.google.com

        res = test_data.add_record(client,"a.b.c",record_type,headers)
        assert res.status_code == 200
        res = json.loads(res.data.decode('utf8'))
        id_record = res['message']['id']
        res = test_data.add_content_data(client,'mail.google.com',id_record,headers)

        data = {"zone-insert": {"tags":{"id_record": id_record}}}
        res = test_data.post_data(client,'sendcommand',data,headers)
        res = json.loads(res.data.decode('utf8'))
        
        # ZONE READ
        id_zone = test_data.identity['zone']['id_zone']
        data = {"zone-read" : {"tags":{"id_zone": id_zone}}}
        res = test_data.post_data(client,'sendcommand',data,headers)
        nm_zone = test_data.identity['zone']['nm_zone']
        res=self.assert_hostname(res,'a.b.c.wetestzone.xyz.',nm_zone)
        self.assert_value(res,'mail.google.com.wetestzone.xyz.',record_type)
        test_data.teardown_record(client,id_record,headers)


        ##### hostname : A-0c  content: mail.google.com.

        res = test_data.add_record(client,"a-0c",record_type,headers)
        assert res.status_code == 200
        res = json.loads(res.data.decode('utf8'))
        id_record = res['message']['id']
        res = test_data.add_content_data(client,'mail.google.com.',id_record,headers)

        data = {"zone-insert": {"tags":{"id_record": id_record}}}
        res = test_data.post_data(client,'sendcommand',data,headers)
        res = json.loads(res.data.decode('utf8'))
        
        # ZONE READ
        id_zone = test_data.identity['zone']['id_zone']
        data = {"zone-read" : {"tags":{"id_zone": id_zone}}}
        res = test_data.post_data(client,'sendcommand',data,headers)
        nm_zone = test_data.identity['zone']['nm_zone']
        res=self.assert_hostname(res,'a-0c.wetestzone.xyz.',nm_zone)
        self.assert_value(res,'mail.google.com.',record_type)
        test_data.teardown_record(client,id_record,headers)


        ##### hostname : 0--0  content: mail.google.com.

        res = test_data.add_record(client,"0--0",record_type,headers)
        assert res.status_code == 200
        res = json.loads(res.data.decode('utf8'))
        id_record = res['message']['id']
        res = test_data.add_content_data(client,'store.cobadns08.xyz',id_record,headers)

        data = {"zone-insert": {"tags":{"id_record": id_record}}}
        res = test_data.post_data(client,'sendcommand',data,headers)
        res = json.loads(res.data.decode('utf8'))
        
        # ZONE READ
        id_zone = test_data.identity['zone']['id_zone']
        data = {"zone-read" : {"tags":{"id_zone": id_zone}}}
        res = test_data.post_data(client,'sendcommand',data,headers)
        nm_zone = test_data.identity['zone']['nm_zone']
        res=self.assert_hostname(res,'0--0.wetestzone.xyz.',nm_zone)
        self.assert_value(res,'store.cobadns08.xyz.wetestzone.xyz.',record_type)
        test_data.teardown_record(client,id_record,headers)

        ########## hostname : @ , content: store.cobadns08.xyz.
        res = test_data.add_record(client,"@",record_type,headers)
        assert res.status_code == 200
        res = json.loads(res.data.decode('utf8'))
        id_record = res['message']['id']
        res = test_data.add_content_data(client,'store.wetestzone.xyz.',id_record,headers)

        data = {"zone-insert": {"tags":{"id_record": id_record}}}
        res = test_data.post_data(client,'sendcommand',data,headers)
        res = json.loads(res.data.decode('utf8'))
        
        # ZONE READ
        id_zone = test_data.identity['zone']['id_zone']
        data = {"zone-read" : {"tags":{"id_zone": id_zone}}}
        res = test_data.post_data(client,'sendcommand',data,headers)
        nm_zone = test_data.identity['zone']['nm_zone']
        respons = self.assert_hostname(res,'wetestzone.xyz.',nm_zone)
        self.assert_value(respons,'store.wetestzone.xyz.',record_type)
        test_data.teardown_record(client,id_record,headers)

        ########## hostname : @ , content: abc.wetestzone.xyz
        
        hostname_ = '@'
        expected_hostname = 'wetestzone.xyz.'
        content_value = 'abc.wetestzone.xyz'
        expected_content_value = 'abc.wetestzone.xyz.wetestzone.xyz.'
        
        res = test_data.add_record(client,hostname_,record_type,headers)
        assert res.status_code == 200
        res = json.loads(res.data.decode('utf8'))
        id_record = res['message']['id']
        res = test_data.add_content_data(client,content_value,id_record,headers)

        data = {"zone-insert": {"tags":{"id_record": id_record}}}
        res = test_data.post_data(client,'sendcommand',data,headers)
        res = json.loads(res.data.decode('utf8'))
        
        # ZONE READ
        id_zone = test_data.identity['zone']['id_zone']
        data = {"zone-read" : {"tags":{"id_zone": id_zone}}}
        res = test_data.post_data(client,'sendcommand',data,headers)
        nm_zone = test_data.identity['zone']['nm_zone']
        respons = self.assert_hostname(res,expected_hostname,nm_zone)
        self.assert_value(respons,expected_content_value,record_type)
        test_data.teardown_record(client,id_record,headers)


        ########## hostname : @ , content: a.b.c.wetestzone.xyz.
        
        hostname_ = '@'
        expected_hostname = 'wetestzone.xyz.'
        content_value = 'abc.wetestzone.xyz.'
        expected_content_value = 'abc.wetestzone.xyz.'
        
        res = test_data.add_record(client,hostname_,record_type,headers)
        assert res.status_code == 200
        res = json.loads(res.data.decode('utf8'))
        id_record = res['message']['id']
        res = test_data.add_content_data(client,content_value,id_record,headers)

        data = {"zone-insert": {"tags":{"id_record": id_record}}}
        res = test_data.post_data(client,'sendcommand',data,headers)
        res = json.loads(res.data.decode('utf8'))
        
        # ZONE READ
        id_zone = test_data.identity['zone']['id_zone']
        data = {"zone-read" : {"tags":{"id_zone": id_zone}}}
        res = test_data.post_data(client,'sendcommand',data,headers)
        nm_zone = test_data.identity['zone']['nm_zone']
        respons = self.assert_hostname(res,expected_hostname,nm_zone)
        self.assert_value(respons,expected_content_value,record_type)
        test_data.teardown_record(client,id_record,headers)

        ########## hostname : @ , content: a.b.c.wetestzone.xyz.
        
        hostname_ = '@'
        expected_hostname = 'wetestzone.xyz.'
        content_value = 'abc.wetestzone.xyz.'
        expected_content_value = 'abc.wetestzone.xyz.'
        
        res = test_data.add_record(client,hostname_,record_type,headers)
        assert res.status_code == 200
        res = json.loads(res.data.decode('utf8'))
        id_record = res['message']['id']
        res = test_data.add_content_data(client,content_value,id_record,headers)

        data = {"zone-insert": {"tags":{"id_record": id_record}}}
        res = test_data.post_data(client,'sendcommand',data,headers)
        res = json.loads(res.data.decode('utf8'))
        
        # ZONE READ
        id_zone = test_data.identity['zone']['id_zone']
        data = {"zone-read" : {"tags":{"id_zone": id_zone}}}
        res = test_data.post_data(client,'sendcommand',data,headers)
        nm_zone = test_data.identity['zone']['nm_zone']
        respons = self.assert_hostname(res,expected_hostname,nm_zone)
        self.assert_value(respons,expected_content_value,record_type)
        test_data.teardown_record(client,id_record,headers)

        ########## hostname : @ , content: mail
        
        hostname_ = '@'
        expected_hostname = 'wetestzone.xyz.'
        content_value = 'mail'
        expected_content_value = 'mail.wetestzone.xyz.'
        
        res = test_data.add_record(client,hostname_,record_type,headers)
        assert res.status_code == 200
        res = json.loads(res.data.decode('utf8'))
        id_record = res['message']['id']
        res = test_data.add_content_data(client,content_value,id_record,headers)

        data = {"zone-insert": {"tags":{"id_record": id_record}}}
        res = test_data.post_data(client,'sendcommand',data,headers)
        res = json.loads(res.data.decode('utf8'))
        
        # ZONE READ
        id_zone = test_data.identity['zone']['id_zone']
        data = {"zone-read" : {"tags":{"id_zone": id_zone}}}
        res = test_data.post_data(client,'sendcommand',data,headers)
        nm_zone = test_data.identity['zone']['nm_zone']
        respons = self.assert_hostname(res,expected_hostname,nm_zone)
        self.assert_value(respons,expected_content_value,record_type)
        test_data.teardown_record(client,id_record,headers)

        ########## hostname : @ , content: A-0c
        
        hostname_ = '@'
        expected_hostname = 'wetestzone.xyz.'
        content_value = 'A-0c'
        expected_content_value = 'a-0c.wetestzone.xyz.'
        
        res = test_data.add_record(client,hostname_,record_type,headers)
        assert res.status_code == 200
        res = json.loads(res.data.decode('utf8'))
        id_record = res['message']['id']
        res = test_data.add_content_data(client,content_value,id_record,headers)

        data = {"zone-insert": {"tags":{"id_record": id_record}}}
        res = test_data.post_data(client,'sendcommand',data,headers)
        res = json.loads(res.data.decode('utf8'))
        
        # ZONE READ
        id_zone = test_data.identity['zone']['id_zone']
        data = {"zone-read" : {"tags":{"id_zone": id_zone}}}
        res = test_data.post_data(client,'sendcommand',data,headers)
        nm_zone = test_data.identity['zone']['nm_zone']
        respons = self.assert_hostname(res,expected_hostname,nm_zone)
        self.assert_value(respons,expected_content_value,record_type)
        test_data.teardown_record(client,id_record,headers)

        ########## hostname : @ , content: o12345670123456701234567012345670123456701234567012345670123456
        
        hostname_ = '@'
        expected_hostname = 'wetestzone.xyz.'
        content_value = 'o12345670123456701234567012345670123456701234567012345670123456'
        expected_content_value = 'o12345670123456701234567012345670123456701234567012345670123456.wetestzone.xyz.'
        
        res = test_data.add_record(client,hostname_,record_type,headers)
        assert res.status_code == 200
        res = json.loads(res.data.decode('utf8'))
        id_record = res['message']['id']
        res = test_data.add_content_data(client,content_value,id_record,headers)

        data = {"zone-insert": {"tags":{"id_record": id_record}}}
        res = test_data.post_data(client,'sendcommand',data,headers)
        res = json.loads(res.data.decode('utf8'))
        
        # ZONE READ
        id_zone = test_data.identity['zone']['id_zone']
        data = {"zone-read" : {"tags":{"id_zone": id_zone}}}
        res = test_data.post_data(client,'sendcommand',data,headers)
        nm_zone = test_data.identity['zone']['nm_zone']
        respons = self.assert_hostname(res,expected_hostname,nm_zone)
        self.assert_value(respons,expected_content_value,record_type)
        test_data.teardown_record(client,id_record,headers)

        ########## FAILURE hostname : @ , content: -A0c
        
        hostname_ = '@'
        expected_hostname = 'wetestzone.xyz.'
        content_value = '-A0c'
        
        res = test_data.add_record(client,hostname_,record_type,headers)
        assert res.status_code == 200
        res = json.loads(res.data.decode('utf8'))
        id_record = res['message']['id']
        res = test_data.add_content_data_fail(client,content_value,id_record,headers)

        ########## FAILURE hostname : @ , content: A0c-
        
        hostname_ = '@'
        expected_hostname = 'wetestzone.xyz.'
        content_value = 'A0c-'
        
        res = test_data.add_record(client,hostname_,record_type,headers)
        assert res.status_code == 200
        res = json.loads(res.data.decode('utf8'))
        id_record = res['message']['id']
        res = test_data.add_content_data_fail(client,content_value,id_record,headers)

        ########## FAILURE hostname : @ , content: A.-0c
        
        hostname_ = '@'
        expected_hostname = 'wetestzone.xyz.'
        content_value = 'A.-0c'
        
        res = test_data.add_record(client,hostname_,record_type,headers)
        assert res.status_code == 200
        res = json.loads(res.data.decode('utf8'))
        id_record = res['message']['id']
        res = test_data.add_content_data_fail(client,content_value,id_record,headers)

        ########## FAILURE hostname : @ , content: A-.0c
        
        hostname_ = '@'
        expected_hostname = 'wetestzone.xyz.'
        content_value = 'A-.0c'
        
        res = test_data.add_record(client,hostname_,record_type,headers)
        assert res.status_code == 200
        res = json.loads(res.data.decode('utf8'))
        id_record = res['message']['id']
        res = test_data.add_content_data_fail(client,content_value,id_record,headers)


        ########## FAILURE hostname : @ , content: o123456701234567012345670123456701234567012345670123456701234567
        
        hostname_ = '@'
        expected_hostname = 'wetestzone.xyz.'
        content_value = 'o123456701234567012345670123456701234567012345670123456701234567'
        
        res = test_data.add_record(client,hostname_,record_type,headers)
        assert res.status_code == 200
        res = json.loads(res.data.decode('utf8'))
        id_record = res['message']['id']
        res = test_data.add_content_data_fail(client,content_value,id_record,headers)

        ########## FAILURE hostname : www.
        
        hostname_ = 'www.'
        expected_hostname = 'wetestzone.xyz.'
        content_value = 'o123456701234567012345670123456701234567012345670123456701234567'
        
        res = test_data.add_error_record(client,hostname_,record_type,headers)

        ########## FAILURE hostname : mail.cobadns08.xyz.
        
        hostname_ = 'mail.cobadns08.xyz.'
        res = test_data.add_error_record(client,hostname_,record_type,headers)

        ########## FAILURE hostname : *
        
        hostname_ = '*'        
        res = test_data.add_error_record(client,hostname_,record_type,headers)

        ########## FAILURE hostname : -A0c
        
        hostname_ = '-A0c'        
        res = test_data.add_error_record(client,hostname_,record_type,headers)

        ########## FAILURE hostname : A0c-
        
        hostname_ = '-A0c-'        
        res = test_data.add_error_record(client,hostname_,record_type,headers)

        ########## FAILURE hostname : A.-0c
        
        hostname_ = 'A.-0c'        
        res = test_data.add_error_record(client,hostname_,record_type,headers)

        ########## FAILURE hostname : A-.0c
        
        hostname_ = 'A-.0c'        
        res = test_data.add_error_record(client,hostname_,record_type,headers)

        ########## FAILURE hostname : o123456701234567012345670123456701234567012345670123456701234567
        
        hostname_ = 'o123456701234567012345670123456701234567012345670123456701234567'        
        res = test_data.add_error_record(client,hostname_,record_type,headers)

        ########## hostname : @ , content: a.b.c.wetestzone.xyz. EDITING RECORD
        
        hostname_ = '@'
        expected_hostname = 'test.wetestzone.xyz.'
        content_value = 'abc.wetestzone.xyz.'
        expected_content_value = 'bvrtan.wetestzone.xyz.'
        
        res = test_data.add_record(client,hostname_,record_type,headers)
        assert res.status_code == 200
        res = json.loads(res.data.decode('utf8'))
        id_record = res['message']['id']
        res = test_data.add_content_data(client,content_value,id_record,headers)
        id_content = res['id_content']
        id_ttldata = res['id_ttldata']
        data = {"zone-insert": {"tags":{"id_record": id_record}}}
        res = test_data.post_data(client,'sendcommand',data,headers)
        res = json.loads(res.data.decode('utf8'))
        

        ## EDIT DATA
        res = test_data.edit_ttldata(client,id_ttldata,'402428102489735169',id_record,headers)
        assert res.status_code == 200
        res = test_data.edit_content_data(client,id_content,id_record,'bvrtan.wetestzone.xyz.',headers)
        assert res.status_code == 200
        new_data = {
            "nm_record" : "test",
            "id_type" : "402427533112147969",
            "id_zone": id_zone,
            "date_record": "20190707"
        }
        res = test_data.edit_record(client,id_record,new_data,headers)

        # ZONE READ
        id_zone = test_data.identity['zone']['id_zone']
        data = {"zone-read" : {"tags":{"id_zone": id_zone}}}
        res = test_data.post_data(client,'sendcommand',data,headers)
        nm_zone = test_data.identity['zone']['nm_zone']
        respons = self.assert_hostname(res,expected_hostname,nm_zone)
        self.assert_value(respons,expected_content_value,record_type)
        test_data.teardown_record(client,id_record,headers)


        test_data.teardown(client,headers)
        self.testset.remove(test_data)

    def test_mx(self,client,get_header):
        record_type = 'mx'

        priority = '10'

        headers = get_header
        test_data = DataTest()
        self.testset.append(test_data)
        res = test_data.add_zone(client,"wetestzone.xyz",headers)
        assert res.status_code == 200
        
        ########## hostname : @ , content: wetestzone.xyz
        
        hostname = '@'
        expected_hostname = 'wetestzone.xyz.'
        content_serial = 'wetestzone.xyz'
        expected_content_serial = priority + ' wetestzone.xyz.wetestzone.xyz.'
        
        res = test_data.add_record(client,hostname,record_type,headers)
        assert res.status_code == 200
        res = json.loads(res.data.decode('utf8'))
        id_record = res['message']['id']
        res = test_data.add_content_data(client,priority,id_record,headers)
        res = test_data.add_content_serial(client,content_serial,id_record,headers)

        data = {"zone-insert": {"tags":{"id_record": id_record}}}
        res = test_data.post_data(client,'sendcommand',data,headers)
        res = json.loads(res.data.decode('utf8'))
        
        # ZONE READ
        id_zone = test_data.identity['zone']['id_zone']
        data = {"zone-read" : {"tags":{"id_zone": id_zone}}}
        res = test_data.post_data(client,'sendcommand',data,headers)
        tmp = json.loads(res.data.decode('utf8')) 
        nm_zone = test_data.identity['zone']['nm_zone']
        respons = self.assert_hostname(res,expected_hostname,nm_zone)
        self.assert_value(respons,expected_content_serial,record_type)
        
        ############## hostname : wetestzone.xyz , content : wetestzone.xyz.    
        hostname = 'wetestzone.xyz'
        expected_hostname = 'wetestzone.xyz.wetestzone.xyz.'
        content_serial = 'wetestzone.xyz.'
        expected_content_serial = priority + ' wetestzone.xyz.'
        
        res = test_data.add_record(client,hostname,record_type,headers)
        assert res.status_code == 200
        res = json.loads(res.data.decode('utf8'))
        id_record = res['message']['id']
        res = test_data.add_content_data(client,priority,id_record,headers)
        res = test_data.add_content_serial(client,content_serial,id_record,headers)

        data = {"zone-insert": {"tags":{"id_record": id_record}}}
        res = test_data.post_data(client,'sendcommand',data,headers)
        res = json.loads(res.data.decode('utf8'))
        
        # ZONE READ
        id_zone = test_data.identity['zone']['id_zone']
        data = {"zone-read" : {"tags":{"id_zone": id_zone}}}
        res = test_data.post_data(client,'sendcommand',data,headers)
        tmp = json.loads(res.data.decode('utf8')) 
        nm_zone = test_data.identity['zone']['nm_zone']
        respons = self.assert_hostname(res,expected_hostname,nm_zone)
        self.assert_value(respons,expected_content_serial,record_type)
        
        
        ##### hostname : www , content: @
        hostname = 'www'
        expected_hostname = 'www.wetestzone.xyz.'
        content_serial = '@'
        expected_content_serial = priority + ' wetestzone.xyz.'

        res = test_data.add_record(client,hostname,record_type,headers)
        assert res.status_code == 200
        res = json.loads(res.data.decode('utf8'))
        id_record = res['message']['id']
        res = test_data.add_content_data(client,priority,id_record,headers)
        res = test_data.add_content_serial(client,content_serial,id_record,headers)

        data = {"zone-insert": {"tags":{"id_record": id_record}}}
        res = test_data.post_data(client,'sendcommand',data,headers)
        res = json.loads(res.data.decode('utf8'))
        
        # ZONE READ
        id_zone = test_data.identity['zone']['id_zone']
        data = {"zone-read" : {"tags":{"id_zone": id_zone}}}
        res = test_data.post_data(client,'sendcommand',data,headers)
        tmp = json.loads(res.data.decode('utf8')) 
        nm_zone = test_data.identity['zone']['nm_zone']
        respons = self.assert_hostname(res,expected_hostname,nm_zone)
        self.assert_value(respons,expected_content_serial,record_type)

        ##### hostname : a.b.c  content: mail.google.com
        hostname = 'a.b.c'
        expected_hostname = 'a.b.c.wetestzone.xyz.'
        content_serial = 'mail.google.com'
        expected_content_serial = priority + ' mail.google.com.wetestzone.xyz.'

        res = test_data.add_record(client,hostname,record_type,headers)
        assert res.status_code == 200
        res = json.loads(res.data.decode('utf8'))
        id_record = res['message']['id']
        res = test_data.add_content_data(client,priority,id_record,headers)
        res = test_data.add_content_serial(client,content_serial,id_record,headers)

        data = {"zone-insert": {"tags":{"id_record": id_record}}}
        res = test_data.post_data(client,'sendcommand',data,headers)
        res = json.loads(res.data.decode('utf8'))
        
        # ZONE READ
        id_zone = test_data.identity['zone']['id_zone']
        data = {"zone-read" : {"tags":{"id_zone": id_zone}}}
        res = test_data.post_data(client,'sendcommand',data,headers)
        tmp = json.loads(res.data.decode('utf8')) 
        nm_zone = test_data.identity['zone']['nm_zone']
        respons = self.assert_hostname(res,expected_hostname,nm_zone)
        self.assert_value(respons,expected_content_serial,record_type)

        ##### hostname : A-0c  content: mail.google.com.

        hostname = 'A-0c'
        expected_hostname = 'a-0c.wetestzone.xyz.'
        content_serial = 'mail.google.com.'
        expected_content_serial = priority + ' mail.google.com.'

        res = test_data.add_record(client,hostname,record_type,headers)
        assert res.status_code == 200
        res = json.loads(res.data.decode('utf8'))
        id_record = res['message']['id']
        res = test_data.add_content_data(client,priority,id_record,headers)
        res = test_data.add_content_serial(client,content_serial,id_record,headers)

        data = {"zone-insert": {"tags":{"id_record": id_record}}}
        res = test_data.post_data(client,'sendcommand',data,headers)
        res = json.loads(res.data.decode('utf8'))
        
        # ZONE READ
        id_zone = test_data.identity['zone']['id_zone']
        data = {"zone-read" : {"tags":{"id_zone": id_zone}}}
        res = test_data.post_data(client,'sendcommand',data,headers)
        tmp = json.loads(res.data.decode('utf8')) 
        nm_zone = test_data.identity['zone']['nm_zone']
        respons = self.assert_hostname(res,expected_hostname,nm_zone)
        self.assert_value(respons,expected_content_serial,record_type)


        ##### hostname : 0--0  content: mail.google.com.

        hostname = '0--0'
        expected_hostname = '0--0.wetestzone.xyz.'
        content_serial = 'mail.google.com.'
        expected_content_serial = priority + ' mail.google.com.'

        res = test_data.add_record(client,hostname,record_type,headers)
        assert res.status_code == 200
        res = json.loads(res.data.decode('utf8'))
        id_record = res['message']['id']
        res = test_data.add_content_data(client,priority,id_record,headers)
        res = test_data.add_content_serial(client,content_serial,id_record,headers)

        data = {"zone-insert": {"tags":{"id_record": id_record}}}
        res = test_data.post_data(client,'sendcommand',data,headers)
        res = json.loads(res.data.decode('utf8'))
        
        # ZONE READ
        id_zone = test_data.identity['zone']['id_zone']
        data = {"zone-read" : {"tags":{"id_zone": id_zone}}}
        res = test_data.post_data(client,'sendcommand',data,headers)
        tmp = json.loads(res.data.decode('utf8')) 
        nm_zone = test_data.identity['zone']['nm_zone']
        respons = self.assert_hostname(res,expected_hostname,nm_zone)
        self.assert_value(respons,expected_content_serial,record_type)

        ########## hostname : @ , content: store.cobadns08.xyz.

        hostname = '@'
        expected_hostname = 'wetestzone.xyz.'
        content_serial = 'store.wetestzone.xyz.'
        expected_content_serial = priority + ' store.wetestzone.xyz.'

        res = test_data.add_record(client,hostname,record_type,headers)
        assert res.status_code == 200
        res = json.loads(res.data.decode('utf8'))
        id_record = res['message']['id']
        res = test_data.add_content_data(client,priority,id_record,headers)
        res = test_data.add_content_serial(client,content_serial,id_record,headers)

        data = {"zone-insert": {"tags":{"id_record": id_record}}}
        res = test_data.post_data(client,'sendcommand',data,headers)
        res = json.loads(res.data.decode('utf8'))
        
        # ZONE READ
        id_zone = test_data.identity['zone']['id_zone']
        data = {"zone-read" : {"tags":{"id_zone": id_zone}}}
        res = test_data.post_data(client,'sendcommand',data,headers)
        tmp = json.loads(res.data.decode('utf8')) 
        nm_zone = test_data.identity['zone']['nm_zone']
        respons = self.assert_hostname(res,expected_hostname,nm_zone)
        self.assert_value(respons,expected_content_serial,record_type)

        # ########## hostname : @ , content: abc.wetestzone.xyz

        hostname = '@'
        expected_hostname = 'wetestzone.xyz.'
        content_serial = 'abc.wetestzone.xyz'
        expected_content_serial = priority + ' abc.wetestzone.xyz.wetestzone.xyz.'

        res = test_data.add_record(client,hostname,record_type,headers)
        assert res.status_code == 200
        res = json.loads(res.data.decode('utf8'))
        id_record = res['message']['id']
        res = test_data.add_content_data(client,priority,id_record,headers)
        res = test_data.add_content_serial(client,content_serial,id_record,headers)

        data = {"zone-insert": {"tags":{"id_record": id_record}}}
        res = test_data.post_data(client,'sendcommand',data,headers)
        res = json.loads(res.data.decode('utf8'))
        
        # ZONE READ
        id_zone = test_data.identity['zone']['id_zone']
        data = {"zone-read" : {"tags":{"id_zone": id_zone}}}
        res = test_data.post_data(client,'sendcommand',data,headers)
        tmp = json.loads(res.data.decode('utf8')) 
        nm_zone = test_data.identity['zone']['nm_zone']
        respons = self.assert_hostname(res,expected_hostname,nm_zone)
        self.assert_value(respons,expected_content_serial,record_type)


        # ########## hostname : @ , content: a.b.c.wetestzone.xyz
        hostname = '@'
        expected_hostname = 'wetestzone.xyz.'
        content_serial = 'abc.wetestzone.xyz.'
        expected_content_serial = priority + ' abc.wetestzone.xyz.'

        res = test_data.add_record(client,hostname,record_type,headers)
        assert res.status_code == 200
        res = json.loads(res.data.decode('utf8'))
        id_record = res['message']['id']
        res = test_data.add_content_data(client,priority,id_record,headers)
        res = test_data.add_content_serial(client,content_serial,id_record,headers)

        data = {"zone-insert": {"tags":{"id_record": id_record}}}
        res = test_data.post_data(client,'sendcommand',data,headers)
        res = json.loads(res.data.decode('utf8'))
        
        # ZONE READ
        id_zone = test_data.identity['zone']['id_zone']
        data = {"zone-read" : {"tags":{"id_zone": id_zone}}}
        res = test_data.post_data(client,'sendcommand',data,headers)
        tmp = json.loads(res.data.decode('utf8')) 
        nm_zone = test_data.identity['zone']['nm_zone']
        respons = self.assert_hostname(res,expected_hostname,nm_zone)
        self.assert_value(respons,expected_content_serial,record_type)


        # ########## hostname : @ , content: mail
        
        # hostname_ = '@'
        # expected_hostname = 'wetestzone.xyz.'
        # content_value = 'mail'
        # expected_content_value = 'mail.wetestzone.xyz.'
        
        hostname = '@'
        expected_hostname = 'wetestzone.xyz.'
        content_serial = 'mail'
        expected_content_serial = priority + ' mail.wetestzone.xyz.'

        res = test_data.add_record(client,hostname,record_type,headers)
        assert res.status_code == 200
        res = json.loads(res.data.decode('utf8'))
        id_record = res['message']['id']
        res = test_data.add_content_data(client,priority,id_record,headers)
        res = test_data.add_content_serial(client,content_serial,id_record,headers)

        data = {"zone-insert": {"tags":{"id_record": id_record}}}
        res = test_data.post_data(client,'sendcommand',data,headers)
        res = json.loads(res.data.decode('utf8'))
        
        # ZONE READ
        id_zone = test_data.identity['zone']['id_zone']
        data = {"zone-read" : {"tags":{"id_zone": id_zone}}}
        res = test_data.post_data(client,'sendcommand',data,headers)
        tmp = json.loads(res.data.decode('utf8')) 
        nm_zone = test_data.identity['zone']['nm_zone']
        respons = self.assert_hostname(res,expected_hostname,nm_zone)
        self.assert_value(respons,expected_content_serial,record_type)

        # ########## hostname : @ , content: A-0c
        
        # hostname_ = '@'
        # expected_hostname = 'wetestzone.xyz.'
        # content_value = 'A-0c'
        # expected_content_value = 'a-0c.wetestzone.xyz.'
        
        hostname = '@'
        expected_hostname = 'wetestzone.xyz.'
        content_serial = 'A-0c'
        expected_content_serial = priority + ' a-0c.wetestzone.xyz.'

        res = test_data.add_record(client,hostname,record_type,headers)
        assert res.status_code == 200
        res = json.loads(res.data.decode('utf8'))
        id_record = res['message']['id']
        res = test_data.add_content_data(client,priority,id_record,headers)
        res = test_data.add_content_serial(client,content_serial,id_record,headers)

        data = {"zone-insert": {"tags":{"id_record": id_record}}}
        res = test_data.post_data(client,'sendcommand',data,headers)
        res = json.loads(res.data.decode('utf8'))
        
        # ZONE READ
        id_zone = test_data.identity['zone']['id_zone']
        data = {"zone-read" : {"tags":{"id_zone": id_zone}}}
        res = test_data.post_data(client,'sendcommand',data,headers)
        tmp = json.loads(res.data.decode('utf8')) 
        nm_zone = test_data.identity['zone']['nm_zone']
        respons = self.assert_hostname(res,expected_hostname,nm_zone)
        self.assert_value(respons,expected_content_serial,record_type)

        # ########## hostname : @ , content: o12345670123456701234567012345670123456701234567012345670123456
        
        # hostname_ = '@'
        # expected_hostname = 'wetestzone.xyz.'
        # content_value = 'o12345670123456701234567012345670123456701234567012345670123456'
        # expected_content_value = 'o12345670123456701234567012345670123456701234567012345670123456.wetestzone.xyz.'
        
        hostname = '@'
        expected_hostname = 'wetestzone.xyz.'
        content_serial = 'o12345670123456701234567012345670123456701234567012345670123456'
        expected_content_serial = priority + ' o12345670123456701234567012345670123456701234567012345670123456.wetestzone.xyz.'

        res = test_data.add_record(client,hostname,record_type,headers)
        assert res.status_code == 200
        res = json.loads(res.data.decode('utf8'))
        id_record = res['message']['id']
        res = test_data.add_content_data(client,priority,id_record,headers)
        res = test_data.add_content_serial(client,content_serial,id_record,headers)

        data = {"zone-insert": {"tags":{"id_record": id_record}}}
        res = test_data.post_data(client,'sendcommand',data,headers)
        res = json.loads(res.data.decode('utf8'))
        
        # ZONE READ
        id_zone = test_data.identity['zone']['id_zone']
        data = {"zone-read" : {"tags":{"id_zone": id_zone}}}
        res = test_data.post_data(client,'sendcommand',data,headers)
        tmp = json.loads(res.data.decode('utf8')) 
        nm_zone = test_data.identity['zone']['nm_zone']
        respons = self.assert_hostname(res,expected_hostname,nm_zone)
        self.assert_value(respons,expected_content_serial,record_type)

        ### TEST VIEW_ALL
        d = {"view_all":{"tags":{"id_record": ""}}}
        res = test_data.post_data(client,'record',d,headers)

        d = {"view_all":{"tags":{"id_zone": id_zone}}}
        res = test_data.post_data(client,'record',d,headers)

        # ########## FAILURE hostname : @ , content: -A0c
        
        hostname_ = '@'
        expected_hostname = 'wetestzone.xyz.'
        content_serial = '-A0c'
        
        res = test_data.add_record(client,hostname_,record_type,headers)
        assert res.status_code == 200
        res = json.loads(res.data.decode('utf8'))
        id_record = res['message']['id']
        res = test_data.add_content_data(client,priority,id_record,headers)
        res = test_data.add_content_serial_fail(client,content_serial,id_record,headers)
        # ########## FAILURE hostname : @ , content: A0c-
        
        hostname_ = '@'
        expected_hostname = 'wetestzone.xyz.'
        content_serial = '-A0c-'
        
        res = test_data.add_record(client,hostname_,record_type,headers)
        assert res.status_code == 200
        res = json.loads(res.data.decode('utf8'))
        id_record = res['message']['id']
        res = test_data.add_content_data(client,priority,id_record,headers)
        res = test_data.add_content_serial_fail(client,content_serial,id_record,headers)

        # ########## FAILURE hostname : @ , content: A.-0c
        
        # hostname_ = '@'
        # expected_hostname = 'wetestzone.xyz.'
        # content_value = 'A.-0c'
        
        hostname_ = '@'
        expected_hostname = 'wetestzone.xyz.'
        content_serial = 'A.-0c'
        
        res = test_data.add_record(client,hostname_,record_type,headers)
        assert res.status_code == 200
        res = json.loads(res.data.decode('utf8'))
        id_record = res['message']['id']
        res = test_data.add_content_data(client,priority,id_record,headers)
        res = test_data.add_content_serial_fail(client,content_serial,id_record,headers)

        # ########## FAILURE hostname : @ , content: A-.0c
        
        # hostname_ = '@'
        # expected_hostname = 'wetestzone.xyz.'
        # content_value = 'A-.0c'
        
        hostname_ = '@'
        expected_hostname = 'wetestzone.xyz.'
        content_serial = 'A-.0c'
        
        res = test_data.add_record(client,hostname_,record_type,headers)
        assert res.status_code == 200
        res = json.loads(res.data.decode('utf8'))
        id_record = res['message']['id']
        res = test_data.add_content_data(client,priority,id_record,headers)
        res = test_data.add_content_serial_fail(client,content_serial,id_record,headers)


        # ########## FAILURE hostname : @ , content: o123456701234567012345670123456701234567012345670123456701234567
        
        # hostname_ = '@'
        # expected_hostname = 'wetestzone.xyz.'
        # content_value = 'o123456701234567012345670123456701234567012345670123456701234567'
        
        hostname_ = '@'
        expected_hostname = 'wetestzone.xyz.'
        content_serial = 'o123456701234567012345670123456701234567012345670123456701234567'
        
        res = test_data.add_record(client,hostname_,record_type,headers)
        assert res.status_code == 200
        res = json.loads(res.data.decode('utf8'))
        id_record = res['message']['id']
        res = test_data.add_content_data(client,priority,id_record,headers)
        res = test_data.add_content_serial_fail(client,content_serial,id_record,headers)

        ########## FAILURE hostname : www.
        
        hostname_ = 'www.'
        expected_hostname = 'wetestzone.xyz.'
        content_value = 'o123456701234567012345670123456701234567012345670123456701234567'
        
        res = test_data.add_error_record(client,hostname_,record_type,headers)

        ########## FAILURE hostname : mail.cobadns08.xyz.
        
        hostname_ = 'mail.cobadns08.xyz.'
        res = test_data.add_error_record(client,hostname_,record_type,headers)

        ########## FAILURE hostname : *
        
        hostname_ = '*'        
        res = test_data.add_error_record(client,hostname_,record_type,headers)

        ########## FAILURE hostname : -A0c
        
        hostname_ = '-A0c'        
        res = test_data.add_error_record(client,hostname_,record_type,headers)

        ########## FAILURE hostname : A0c-
        
        hostname_ = '-A0c-'        
        res = test_data.add_error_record(client,hostname_,record_type,headers)

        ########## FAILURE hostname : A.-0c
        
        hostname_ = 'A.-0c'        
        res = test_data.add_error_record(client,hostname_,record_type,headers)

        ########## FAILURE hostname : A-.0c
        
        hostname_ = 'A-.0c'        
        res = test_data.add_error_record(client,hostname_,record_type,headers)

        ########## FAILURE hostname : o123456701234567012345670123456701234567012345670123456701234567
        
        hostname_ = 'o123456701234567012345670123456701234567012345670123456701234567'        
        res = test_data.add_error_record(client,hostname_,record_type,headers)


        ##### hostname : A-1c  content: mail.google.com.

        hostname = 'A-1c'
        expected_hostname = 'a-1c.wetestzone.xyz.'
        content_serial = 'mail.google.com.'
        expected_content_serial = priority + ' store.google.com.'

        res = test_data.add_record(client,hostname,record_type,headers)
        assert res.status_code == 200
        res = json.loads(res.data.decode('utf8'))
        id_record = res['message']['id']
        res = test_data.add_content_data(client,priority,id_record,headers)
        res = test_data.add_content_serial(client,content_serial,id_record,headers)
        id_content_serial = res['id_content_serial']
        data = {"zone-insert": {"tags":{"id_record": id_record}}}
        res = test_data.post_data(client,'sendcommand',data,headers)
        res = json.loads(res.data.decode('utf8'))
        

        ## EDIT
        new_content = "store.google.com."
        res = test_data.edit_serial_data(client,headers,id_content_serial,id_record,new_content)
        assert res.status_code == 200


        # ZONE READ
        id_zone = test_data.identity['zone']['id_zone']
        data = {"zone-read" : {"tags":{"id_zone": id_zone}}}
        res = test_data.post_data(client,'sendcommand',data,headers)
        tmp = json.loads(res.data.decode('utf8')) 
        nm_zone = test_data.identity['zone']['nm_zone']
        respons = self.assert_hostname(res,expected_hostname,nm_zone)
        self.assert_value(respons,expected_content_serial,record_type)


        test_data.teardown(client,headers)
        self.testset.remove(test_data)

    def test_validation_txt(self,client,get_header):
        record_type = 'txt'

        headers = get_header
        test_data = DataTest()
        self.testset.append(test_data)
        res = test_data.add_zone(client,"wetestzone.xyz",headers)
        assert res.status_code == 200

        ###### hostname : @, content : agus agus
        hostname  = '@'
        expected_hostname = 'wetestzone.xyz.'
        content = "agus agus"
        expected_content = '"agus agus"'

        res = test_data.add_record(client,hostname,record_type,headers)
        assert res.status_code == 200
        res = json.loads(res.data.decode('utf8'))
        id_record = res['message']['id']
        res = test_data.add_content_data(client,content,id_record,headers)
        data = {"zone-insert": {"tags":{"id_record": id_record}}}
        res = test_data.post_data(client,'sendcommand',data,headers)
        res = json.loads(res.data.decode('utf8'))
        
        # ZONE READ
        id_zone = test_data.identity['zone']['id_zone']
        data = {"zone-read" : {"tags":{"id_zone": id_zone}}}
        res = test_data.post_data(client,'sendcommand',data,headers)
        nm_zone = test_data.identity['zone']['nm_zone']
        respons = self.assert_hostname(res,expected_hostname,nm_zone)
        self.assert_value(respons,expected_content,record_type)
        test_data.teardown_record(client,id_record,headers)

        ###### hostname : @, content : agus agus
        hostname  = '@'
        expected_hostname = 'wetestzone.xyz.'
        content = "agus'agus"
        expected_content = '''"agus'agus"'''

        res = test_data.add_record(client,hostname,record_type,headers)
        assert res.status_code == 200
        res = json.loads(res.data.decode('utf8'))
        id_record = res['message']['id']
        res = test_data.add_content_data(client,content,id_record,headers)
        data = {"zone-insert": {"tags":{"id_record": id_record}}}
        res = test_data.post_data(client,'sendcommand',data,headers)
        res = json.loads(res.data.decode('utf8'))
        
        # ZONE READ
        id_zone = test_data.identity['zone']['id_zone']
        data = {"zone-read" : {"tags":{"id_zone": id_zone}}}
        res = test_data.post_data(client,'sendcommand',data,headers)
        nm_zone = test_data.identity['zone']['nm_zone']
        respons = self.assert_hostname(res,expected_hostname,nm_zone)
        self.assert_value(respons,expected_content,record_type)
        test_data.teardown_record(client,id_record,headers)

        ###### hostname : @, content : agus agus
        hostname  = '@'
        expected_hostname = 'wetestzone.xyz.'
        content = """agus"agus"""
        expected_content = '''"agus\\"agus"'''

        res = test_data.add_record(client,hostname,record_type,headers)
        assert res.status_code == 200
        res = json.loads(res.data.decode('utf8'))
        id_record = res['message']['id']
        res = test_data.add_content_data(client,content,id_record,headers)
        data = {"zone-insert": {"tags":{"id_record": id_record}}}
        res = test_data.post_data(client,'sendcommand',data,headers)
        res = json.loads(res.data.decode('utf8'))
        
        # ZONE READ
        id_zone = test_data.identity['zone']['id_zone']
        data = {"zone-read" : {"tags":{"id_zone": id_zone}}}
        res = test_data.post_data(client,'sendcommand',data,headers)
        nm_zone = test_data.identity['zone']['nm_zone']
        respons = self.assert_hostname(res,expected_hostname,nm_zone)
        self.assert_value(respons,expected_content,record_type)
        test_data.teardown_record(client,id_record,headers)

        ###### hostname : @, content : agus agus
        hostname  = '@'
        expected_hostname = 'wetestzone.xyz.'
        content = '"'
        expected_content = '''"\\""'''

        res = test_data.add_record(client,hostname,record_type,headers)
        assert res.status_code == 200
        res = json.loads(res.data.decode('utf8'))
        id_record = res['message']['id']
        res = test_data.add_content_data(client,content,id_record,headers)
        data = {"zone-insert": {"tags":{"id_record": id_record}}}
        res = test_data.post_data(client,'sendcommand',data,headers)
        res = json.loads(res.data.decode('utf8'))
        
        # ZONE READ
        id_zone = test_data.identity['zone']['id_zone']
        data = {"zone-read" : {"tags":{"id_zone": id_zone}}}
        res = test_data.post_data(client,'sendcommand',data,headers)
        nm_zone = test_data.identity['zone']['nm_zone']
        respons = self.assert_hostname(res,expected_hostname,nm_zone)
        self.assert_value(respons,expected_content,record_type)
        test_data.teardown_record(client,id_record,headers)
        
        ###### hostname : @, content : agus agus
        hostname  = '@'
        expected_hostname = 'wetestzone.xyz.'
        content = "'"
        expected_content = '"\'"'

        res = test_data.add_record(client,hostname,record_type,headers)
        assert res.status_code == 200
        res = json.loads(res.data.decode('utf8'))
        id_record = res['message']['id']
        res = test_data.add_content_data(client,content,id_record,headers)
        data = {"zone-insert": {"tags":{"id_record": id_record}}}
        res = test_data.post_data(client,'sendcommand',data,headers)
        res = json.loads(res.data.decode('utf8'))
        
        # ZONE READ
        id_zone = test_data.identity['zone']['id_zone']
        data = {"zone-read" : {"tags":{"id_zone": id_zone}}}
        res = test_data.post_data(client,'sendcommand',data,headers)
        nm_zone = test_data.identity['zone']['nm_zone']
        respons = self.assert_hostname(res,expected_hostname,nm_zone)
        self.assert_value(respons,expected_content,record_type)
        test_data.teardown_record(client,id_record,headers)


        ###### hostname : @, content : agus agus
        hostname  = '@'
        expected_hostname = 'wetestzone.xyz.'
        content = 'Tripping off the beat kinda, dripping off the meat grinder Heat niner, pimping, stripping, soft sweet minor China was a neat signer, trouble with the script Digits double dipped, bubble lipped, subtle lisp midget Borderline schizo, sort of fine tits though'
        expected_content = '"{}" "{}"'.format(content[:255].lower(),content[255:].lower())

        res = test_data.add_record(client,hostname,record_type,headers)
        assert res.status_code == 200
        res = json.loads(res.data.decode('utf8'))
        id_record = res['message']['id']
        res = test_data.add_content_data(client,content,id_record,headers)
        data = {"zone-insert": {"tags":{"id_record": id_record}}}
        res = test_data.post_data(client,'sendcommand',data,headers)
        res = json.loads(res.data.decode('utf8'))
        
        # ZONE READ
        id_zone = test_data.identity['zone']['id_zone']
        data = {"zone-read" : {"tags":{"id_zone": id_zone}}}
        res = test_data.post_data(client,'sendcommand',data,headers)
        nm_zone = test_data.identity['zone']['nm_zone']
        respons = self.assert_hostname(res,expected_hostname,nm_zone)
        self.assert_value(respons,expected_content,record_type)
        test_data.teardown_record(client,id_record,headers)

        ## TEST FAIL

        hostname_ = '@'
        expected_hostname = 'wetestzone.xyz.'
        content_value = '£'
        
        res = test_data.add_record(client,hostname_,record_type,headers)
        assert res.status_code == 200
        res = json.loads(res.data.decode('utf8'))
        id_record = res['message']['id']
        res = test_data.add_content_data_fail(client,content_value,id_record,headers)

        test_data.teardown(client,headers)
        self.testset.remove(test_data)


    def test_validation_a(self,client,get_header):
        
        record_type = 'a'

        headers = get_header
        test_data = DataTest()
        self.testset.append(test_data)
        res = test_data.add_zone(client,"wetestzone.xyz",headers)
        assert res.status_code == 200

        ###### hostname : @, content : agus agus
        hostname  = '@'
        expected_hostname = 'wetestzone.xyz.'
        content = "192.168.1.1"
        expected_content = '192.168.1.1'

        res = test_data.add_record(client,hostname,record_type,headers)
        assert res.status_code == 200
        res = json.loads(res.data.decode('utf8'))
        id_record = res['message']['id']
        res = test_data.add_content_data(client,content,id_record,headers)
        data = {"zone-insert": {"tags":{"id_record": id_record}}}
        res = test_data.post_data(client,'sendcommand',data,headers)
        res = json.loads(res.data.decode('utf8'))
        
        # ZONE READ
        id_zone = test_data.identity['zone']['id_zone']
        data = {"zone-read" : {"tags":{"id_zone": id_zone}}}
        res = test_data.post_data(client,'sendcommand',data,headers)
        nm_zone = test_data.identity['zone']['nm_zone']
        respons = self.assert_hostname(res,expected_hostname,nm_zone)
        self.assert_value(respons,expected_content,record_type)
        test_data.teardown_record(client,id_record,headers)


        ## TEST FAIL

        hostname_ = '@'
        expected_hostname = 'wetestzone.xyz.'
        content_value = 'localhost'
        
        res = test_data.add_record(client,hostname_,record_type,headers)
        assert res.status_code == 200
        res = json.loads(res.data.decode('utf8'))
        id_record = res['message']['id']
        res = test_data.add_content_data_fail(client,content_value,id_record,headers)


        ## TEST FAIL

        hostname_ = '@'
        expected_hostname = 'wetestzone.xyz.'
        content_value = 'sembarangan'
        
        res = test_data.add_record(client,hostname_,record_type,headers)
        assert res.status_code == 200
        res = json.loads(res.data.decode('utf8'))
        id_record = res['message']['id']
        res = test_data.add_content_data_fail(client,content_value,id_record,headers)

        ## TEST FAIL

        hostname_ = '@'
        expected_hostname = 'wetestzone.xyz.'
        content_value = '270.0.0.2'
        
        res = test_data.add_record(client,hostname_,record_type,headers)
        assert res.status_code == 200
        res = json.loads(res.data.decode('utf8'))
        id_record = res['message']['id']
        res = test_data.add_content_data_fail(client,content_value,id_record,headers)

        test_data.teardown(client,headers)
        self.testset.remove(test_data)


    def test_validation_teardown(self,client,get_header):
        headers = get_header
        test_data = self.testset
        if len(test_data) > 0:
            for i in test_data:
                try:
                    i.teardown(client,headers)
                except Exception :
                    pass

