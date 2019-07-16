import pytest
import json
import utils


class Vars:
    ids = dict()
    cleanup_data = dict()

    @property
    def slave(self):
        slave_data = { 
            "nm_slave_node" : "jarjar",
            "ip_slave_node"   : "127.0.0.1",
            "port_slave_node" : "50"}
        return slave_data
    
    @property
    def master(self):
        master_data = { "nm_master" : "quigon",
                "ip_master"   : "192.168.0.0",
                "port" : "6967",
                'nm_config': 'jkt'}
        return master_data

    zone_test = {"nm_zone" : "kalkun.com",
                "id_zone" : "427820188203778049"}



class TestConf:

    mock = Vars()

    def post_data(self,client,endpoint,data,headers=None):
        url = 'api/'+endpoint
        res = client.post(url,data=json.dumps(data),
            content_type = 'application/json', headers=headers)
        
        return res

    @pytest.mark.run(order=1)
    def test_add_slave_master(self,client,get_header):
        
        mock = self.mock
        # GET SLAVE AND MASTER
        head = get_header
        result = client.get('api/slave_node',headers=head)
        assert result.status_code == 200

        result = client.get('api/master',headers=head)
        assert result.status_code == 200


        # ADD MASTER AND SLAVE
        mock_data_master = {
            "insert":{
                "fields": mock.master
            }
        }
        result = self.post_data(client,'master',mock_data_master,headers=head)
        assert result.status_code == 200
        resdata = json.loads(result.data.decode('utf8'))
        print(resdata)
        id_master = resdata['message']['id']
        mock.ids['id_master'] = id_master
        
        tmp_data = mock.slave
        tmp_data['id_master'] = id_master
        mock_data_slave = utils.get_model('add',tmp_data)
        result = self.post_data(client,'slave_node',mock_data_slave,head)
        assert result.status_code == 200
        resdata = json.loads(result.data.decode('utf8'))
        id_cs_slave_node = resdata['message']['id']
        mock.ids['id_cs_slave_node'] = id_cs_slave_node

        #VALIDATE IF DATA IS ON DB

        search = {"id_master": id_master}
        send_data = utils.get_model("where",search)
        result = self.post_data(client,'master',send_data,head)
        assert result.status_code == 200
        see_data = json.loads(result.data.decode('utf8'))
        assert see_data['data'][0]['id_master'] == id_master

        search = {"id_cs_slave_node" : id_cs_slave_node}
        send_data = utils.get_model("where",search)
        result = self.post_data(client,'slave_node',send_data,head)
        assert result.status_code == 200
        see_data = json.loads(result.data.decode('utf8'))
        assert see_data['data'][0]['id_cs_slave_node'] == id_cs_slave_node


        ## REMOVE DATA
        delete = {"id_master": id_master}
        send_data = utils.get_model("remove",delete)
        result = self.post_data(client,'master',send_data,head)
        assert result.status_code == 200
        delete = {"id_cs_slave_node": id_cs_slave_node}
        send_data = utils.get_model("remove",delete)
        result = self.post_data(client,'slave_node',send_data,head)
        assert result.status_code == 200

        ## VALIDATE IF DATA IS REMOVED
        result = client.get('api/master',headers=head)
        data_master = json.loads(result.data.decode('utf8'))
        data_master = data_master['data']
        data_master = [i['id_master'] for i in data_master]
        print(data_master)
        assert id_master not in data_master

        result = client.get('api/slave_node',headers=head)
        data_slave = json.loads(result.data.decode('utf8'))
        data_slave = data_slave['data']
        data_slave = [i['id_cs_slave_node'] for i in data_slave]
        print(data_slave)
        assert id_master not in data_master
    # def test_1slave_get(self,client,get_header):
    #     head = get_header
    #     result = client.get('api/slave_node',headers=head)
        
    #     assert result.status_code == 200

    # @pytest.mark.run(order=2)
    # def test_2slave_create(self,client,get_header):
    #     head = get_header
    #     # REMOVE SLAVE IF EXIST       
    #     try:
    #         fields = {"nm_slave_node": self.mock.slave['name'], "ip_slave_node" : self.mock.slave['ip'], "port_slave_node": self.mock.slave['port']}
    #         data = utils.get_model('add',fields)
    #         res = self.post_data(client,'slave_node',data,head)
    #         assert res.status_code == 200
    #         res = json.loads(res.data.decode('utf8'))
    #         self.mock.slave["id_slave"] = res['message']['id']
    #     except KeyError:
    #         data = utils.get_model('where',{"nm_slave" : self.mock.slave['name']})
    #         res = self.post_data(client,'slave_node',data,head)
    #         res = json.loads(res.data.decode('utf8'))
    #         self.mock.slave["id_slave"] = res['message']['id']

    #     ## Assert if data is True, search slave by name

    #     data = utils.get_model('where',{"nm_slave" : self.mock.slave['name']})
    #     res = self.post_data(client,'slave_node',data,head)

    #     assert res.status_code == 200
    #     res = json.loads(res.data.decode('utf8'))
    #     assert res['data']

    # @pytest.mark.run(order=3)
    # def test_3create_master(self,client,get_header,get_mock):
    #     nm_zone = get_mock['nm_zone']
    #     head = get_header

    #     try:
    #         data = utils.get_model('add',{"nm_zone": nm_zone})
    #         result = self.post_data(client,'zone',data,head)
    #         assert result.status_code == 200
    #         result = json.loads(result.data.decode('utf8'))
    #         self.mock.ids['id_zone'] = result['message']['id']
    #     except KeyError:
    #         data = utils.get_model('where',{"nm_zone": nm_zone})
    #         result = self.post_data(client,'zone',data,head)
    #         assert result.status_code == 200
    #         result = json.loads(result.data.decode('utf8'))
    #         self.mock.ids['id_zone'] = result['data'][0]['id_zone']

    #     m_data = self.mock.master
    #     f_master = {"nm_master" : m_data['name'], "ip_master": m_data['ip'], "port" : m_data['port']}
    #     data = utils.get_model('add',f_master)
    #     result = self.post_data(client,'master',data,head)
    #     assert result.status_code == 200
        
    #     result = json.loads(result.data.decode('utf8'))
    #     self.mock.master['id_master'] = result['message']['id']
    #     ## Confirm if data is true

    #     data = utils.get_model('where',{"nm_master": m_data['name']})
    #     result = self.post_data(client,'master',data,head)
    #     assert result.status_code == 200
    #     result = json.loads(result.data.decode('utf8'))
    #     assert result['data']

    # @pytest.mark.run(order=4)
    # def test_4add_acl_notify_master(self,client,get_header):

    #     head = get_header
    #     id_zone = self.mock.ids['id_zone']
    #     id_master = self.mock.master['id_master']
    #     data = utils.get_model('add',{"id_zone": id_zone, "id_master": id_master})
    #     res = self.post_data(client,'acl_master',data,head)
    #     assert res.status_code == 200
    #     res = json.loads(res.data.decode('utf8'))

    #     id_acl_master = res['message']['id']
    #     self.mock.ids['id_acl_master'] = id_acl_master


    #     res = client.get('api/acl_master',headers=head)
        
    #     assert res.status_code == 200

    #     data = utils.get_model('where',{"id_acl_master": id_acl_master})
    #     res = self.post_data(client,'acl_master',data,head)

    #     assert res.status_code == 200
    #     res = json.loads(res.data.decode('utf8'))
    #     assert res['data']
        
    #     #### notify

    #     data = utils.get_model('add', {"id_zone": id_zone, "id_master": id_master})
    #     res = self.post_data(client,'notify_master',data,head)
    #     assert res.status_code == 200

    #     res = json.loads(res.data.decode('utf8'))
    #     id_notify_master = res['message']['id']
    #     self.mock.ids['id_notify_master'] = id_notify_master

    #     res = client.get('api/notify_master',headers=head)
    #     assert res.status_code == 200

    #     data = utils.get_model('where',{"id_notify_master": id_notify_master})
    #     res = self.post_data(client,'notify_master',data,head)
    #     assert res.status_code == 200
    #     res = json.loads(res.data.decode('utf8'))
    #     assert res['data']

    #     ## REMOVE 

    # @pytest.mark.run(order=5)
    # def test_5add_acl_notify_slave(self,client,get_header):

    #     head = get_header
    #     id_acl_master = self.mock.ids['id_acl_master']
    #     id_slave = self.mock.slave['id_slave']
    #     data = utils.get_model('add',{"id_slave": id_slave, "id_acl_master": id_acl_master})
    #     res = self.post_data(client,'acl_slave',data,head)
    #     assert res.status_code == 200
    #     res = json.loads(res.data.decode('utf8'))
    #     id_acl_slave = res['message']['id']
    #     self.mock.ids['id_acl_slave'] = id_acl_slave


    #     res = client.get('api/acl_slave',headers=head)
        
    #     assert res.status_code == 200

    #     data = utils.get_model('where',{"id_acl_slave": id_acl_slave})
    #     res = self.post_data(client,'acl_slave',data,head)

    #     assert res.status_code == 200
    #     res = json.loads(res.data.decode('utf8'))
    #     assert res['data']
        
    #     #### notify

    #     id_notify_master = self.mock.ids['id_notify_master']
    #     id_zone = self.mock.ids['id_zone']

    #     data = utils.get_model('add', {"id_slave": id_slave, "id_notify_master": id_notify_master})
    #     res = self.post_data(client,'notify_slave',data,head)
    #     assert res.status_code == 200

    #     res = json.loads(res.data.decode('utf8'))
    #     id_notify_slave = res['message']['id']
    #     self.mock.ids['id_notify_slave'] = id_notify_slave

    #     res = client.get('api/notify_slave',headers=head)
    #     assert res.status_code == 200

    #     data = utils.get_model('where',{"id_notify_slave": id_notify_slave})
    #     res = self.post_data(client,'notify_slave',data,head)
    #     assert res.status_code == 200
    #     res = json.loads(res.data.decode('utf8'))
    #     assert res['data']

    #     ## REMOVE 

    #     id_master = self.mock.master['id_master']

    #     header = get_header
    #     fields = {"nm_slave": self.mock.slave['name']}
    #     data = utils.get_model('where',fields)
    #     res = self.post_data(client,api/slave_node,data,header)


    #     data = utils.get_model('remove',{"id_acl_slave": id_acl_slave})
    #     res = self.post_data(client, 'acl_slave', data, head)
    #     assert res.status_code == 200

    #     data = utils.get_model('remove',{"id_notify_slave": id_notify_slave})
    #     res = self.post_data(client, 'notify_slave', data, head)
    #     assert res.status_code == 200

    #     data = utils.get_model('remove',{"id_notify_master": id_notify_master})
    #     res  = self.post_data(client,'notify_master',data,head)
    #     assert res.status_code == 200

    #     data = utils.get_model('remove',{"id_acl_master": id_acl_master})
    #     res = self.post_data(client, 'acl_master', data, head)
    #     assert res.status_code == 200

    #     data = utils.get_model('remove',{"id_slave": id_slave})
    #     res  = self.post_data(client,api/slave_node,data,head)
    #     assert res.status_code == 200       
        
    #     data = utils.get_model('remove',{"id_master": id_master})
    #     res  = self.post_data(client,'master',data,head)
    #     assert res.status_code == 200
        
    #     data = utils.get_model('remove',{"id_zone": id_zone})
    #     res  = self.post_data(client,'zone',data,head)
    #     assert res.status_code == 200

    
    # @pytest.mark.run(order=5)
    # def test_6notify_master(self,client):
    #     """ Before running this test, see id_zone from cs_notify_master on database and use it in this test.
    #     Otherwise, you can skip this test.
    #     """
    #     id_zone = self.mock.zone_test['id_zone']

    #     data_notify = {"master-notify" : {"tags" : {"id_zone" : id_zone}}}
    #     res = self.post_data(client,'sendcommand',data_notify)
    #     assert res.status_code == 200


    #     data_acl = {"master-acl" : {"tags" : { "id_zone" : id_zone}}}
    #     res = self.post_data(client,'sendcommand',data_acl)
    #     assert res.status_code == 200

    #     data_notif_slave = {"slave-notify" : {"tags" : { "id_zone" : id_zone}}}
    #     res = self.post_data(client,'sendcommand',data_notif_slave)
    #     assert res.status_code == 200


    #     data_slave_acl = {"slave-acl" : {"tags" : {"id_zone" : id_zone}}}
    #     res = self.post_data(client,'sendcommand',data_slave_acl)
    #     assert res.status_code == 200

    #     data_file_set = {"file-set" : {"tags" : {"id_zone" : id_zone }}}
    #     res = self.post_data(client,'sendcommand',data_file_set)
    #     assert res.status_code == 200

    #     data_module_set = {"module-set":{"tags":{"id_zone" : id_zone }}}
    #     res = self.post_data(client,'sendcommand',data_module_set)
    #     assert res.status_code == 200

    #     cluster_zone = {"cluster-zone" : {"tags" : {"id_zone" : id_zone}}}
    #     res = self.post_data(client,'sendcommand',cluster_zone)
    #     assert res.status_code == 200

    #     cluster_unset = {"cluster-unset" : {"tags" : {"id_zone" : id_zone}}}
    #     res = self.post_data(client,'sendcommand',cluster_unset)
    #     assert res.status_code == 200

