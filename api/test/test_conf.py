import pytest
import json
import utils


class Vars:
    ids = dict()
    slave = { "name" : "jarjar",
              "ip"   : "127.0.0.1",
              "port" : "50"}
    
    master = { "name" : "quigon",
              "ip"   : "192.168.0.0",
              "port" : "50"}

class TestConf:

    mock = Vars()

    def post_data(self,client,endpoint,data,headers):
        url = 'api/'+endpoint
        res = client.post(url,data=json.dumps(data),
            content_type = 'application/json', headers=headers)
        
        return res

    @pytest.mark.run(order=1)
    def test_slave_get(self,client,get_header):
        print("START")
        head = get_header
        result = client.get('api/slave',headers=head)
        
        assert result.status_code == 200

    @pytest.mark.run(order=2)
    def test_slave_create(self,client,get_header):
        head = get_header
        fields = {"nm_slave": self.mock.slave['name'], "ip_slave" : self.mock.slave['ip'], "port": self.mock.slave['port']}
        data = utils.get_model('add',fields)
        res = self.post_data(client,'slave',data,head)

        assert res.status_code == 200
        res = json.loads(res.data.decode('utf8'))
        self.mock.slave["id_slave"] = res['message']['id']

        ## Assert if data is True, search slave by name

        data = utils.get_model('where',{"nm_slave" : self.mock.slave['name']})
        res = self.post_data(client,'slave',data,head)

        assert res.status_code == 200
        res = json.loads(res.data.decode('utf8'))
        assert res['data']

    @pytest.mark.run(order=3)
    def test_create_master(self,client,get_header,get_mock):
        nm_zone = get_mock['nm_zone']
        head = get_header

        data = utils.get_model('add',{"nm_zone": nm_zone})
        result = self.post_data(client,'zone',data,head)
        assert result.status_code == 200
        result = json.loads(result.data.decode('utf8'))
        self.mock.ids['id_zone'] = result['message']['id']
        
        m_data = self.mock.master
        f_master = {"nm_master" : m_data['name'], "ip_master": m_data['ip'], "port" : m_data['port']}
        data = utils.get_model('add',f_master)
        result = self.post_data(client,'master',data,head)
        assert result.status_code == 200
        
        result = json.loads(result.data.decode('utf8'))
        self.mock.master['id_master'] = result['message']['id']
        ## Confirm if data is true

        data = utils.get_model('where',{"nm_master": m_data['name']})
        result = self.post_data(client,'master',data,head)
        assert result.status_code == 200
        result = json.loads(result.data.decode('utf8'))
        assert result['data']

    @pytest.mark.run(order=4)
    def test_add_acl_notify_master(self,client,get_header):

        head = get_header
        id_zone = self.mock.ids['id_zone']
        id_master = self.mock.master['id_master']
        data = utils.get_model('add',{"id_zone": id_zone, "id_master": id_master})
        res = self.post_data(client,'acl_master',data,head)
        assert res.status_code == 200
        res = json.loads(res.data.decode('utf8'))

        id_acl_master = res['message']['id']
        self.mock.ids['id_acl_master'] = id_acl_master


        res = client.get('api/acl_master',headers=head)
        
        assert res.status_code == 200

        data = utils.get_model('where',{"id_acl_master": id_acl_master})
        res = self.post_data(client,'acl_master',data,head)

        assert res.status_code == 200
        res = json.loads(res.data.decode('utf8'))
        assert res['data']
        
        #### notify

        data = utils.get_model('add', {"id_zone": id_zone, "id_master": id_master})
        res = self.post_data(client,'notify_master',data,head)
        assert res.status_code == 200

        res = json.loads(res.data.decode('utf8'))
        id_notify_master = res['message']['id']
        self.mock.ids['id_notify_master'] = id_notify_master

        res = client.get('api/notify_master',headers=head)
        assert res.status_code == 200

        data = utils.get_model('where',{"id_notify_master": id_notify_master})
        res = self.post_data(client,'notify_master',data,head)
        assert res.status_code == 200
        res = json.loads(res.data.decode('utf8'))
        assert res['data']

        ## REMOVE 

    @pytest.mark.run(order=5)
    def test_add_acl_notify_slave(self,client,get_header):

        head = get_header
        id_acl_master = self.mock.ids['id_acl_master']
        id_slave = self.mock.slave['id_slave']
        data = utils.get_model('add',{"id_slave": id_slave, "id_acl_master": id_acl_master})
        res = self.post_data(client,'acl_slave',data,head)
        assert res.status_code == 200
        res = json.loads(res.data.decode('utf8'))
        id_acl_slave = res['message']['id']
        self.mock.ids['id_acl_slave'] = id_acl_slave


        res = client.get('api/acl_slave',headers=head)
        
        assert res.status_code == 200

        data = utils.get_model('where',{"id_acl_slave": id_acl_slave})
        res = self.post_data(client,'acl_slave',data,head)

        assert res.status_code == 200
        res = json.loads(res.data.decode('utf8'))
        assert res['data']
        
        #### notify

        id_notify_master = self.mock.ids['id_notify_master']
        id_zone = self.mock.ids['id_zone']

        data = utils.get_model('add', {"id_slave": id_slave, "id_notify_master": id_notify_master})
        res = self.post_data(client,'notify_slave',data,head)
        assert res.status_code == 200

        res = json.loads(res.data.decode('utf8'))
        id_notify_slave = res['message']['id']
        self.mock.ids['id_notify_slave'] = id_notify_slave

        res = client.get('api/notify_slave',headers=head)
        assert res.status_code == 200

        data = utils.get_model('where',{"id_notify_slave": id_notify_slave})
        res = self.post_data(client,'notify_slave',data,head)
        assert res.status_code == 200
        res = json.loads(res.data.decode('utf8'))
        assert res['data']

        ## REMOVE 

        id_master = self.mock.master['id_master']


        data = utils.get_model('remove',{"id_acl_slave": id_acl_slave})
        res = self.post_data(client, 'acl_slave', data, head)
        assert res.status_code == 200

        data = utils.get_model('remove',{"id_notify_slave": id_notify_slave})
        res = self.post_data(client, 'notify_slave', data, head)
        assert res.status_code == 200

        data = utils.get_model('remove',{"id_notify_master": id_notify_master})
        res  = self.post_data(client,'notify_master',data,head)
        assert res.status_code == 200

        data = utils.get_model('remove',{"id_acl_master": id_acl_master})
        res = self.post_data(client, 'acl_master', data, head)
        assert res.status_code == 200

        data = utils.get_model('remove',{"id_slave": id_slave})
        res  = self.post_data(client,'slave',data,head)
        assert res.status_code == 200       
        
        data = utils.get_model('remove',{"id_master": id_master})
        res  = self.post_data(client,'master',data,head)
        assert res.status_code == 200
        
        data = utils.get_model('remove',{"id_zone": id_zone})
        res  = self.post_data(client,'zone',data,head)
        assert res.status_code == 200