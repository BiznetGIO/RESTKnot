import pytest
import json
import utils


class Vars:
    ids = dict()


class TestCheckOn:
    var_mock = Vars()

    def post_data(self,client,endpoint,data,headers):
        url = 'api/'+endpoint
        res = client.post(url,data=json.dumps(data),
                    content_type='application/json', headers=headers)
        return res

    def test_cluster_check_master(self,client,get_header,get_mock):
        
        headers = get_header

        # obtain master
        endpoint = 'api/master'
        res = client.get(endpoint,headers=headers)
        res = json.loads(res.data.decode('utf8'))
        id_master = res['data'][0]['id_master']
        self.var_mock.ids['id_master'] = id_master
        endpoint = 'api/cluster/master/{}'.format(id_master)
        res = client.get(endpoint,headers=headers)
        assert res.status_code == 200
        res = json.loads(res.data.decode('utf8'))
        task_id = res['data']['task_id']
        assert str(task_id) == id_master


    def test_cluster_check_slave(self,client,get_header,get_mock):
        
        headers = get_header

        # obtain master
        endpoint = 'api/slave_node'
        res = client.get(endpoint,headers=headers)
        res = json.loads(res.data.decode('utf8'))
        id_cs_slave_node = res['data'][0]['id_cs_slave_node']
        self.var_mock.ids['id_cs_slave_node'] = id_cs_slave_node
        endpoint = 'api/cluster/slave/{}'.format(id_cs_slave_node)
        res = client.get(endpoint,headers=headers)
        assert res.status_code == 200
        res = json.loads(res.data.decode('utf8'))
        task_id = res['data']['task_id']
        assert str(task_id) == id_cs_slave_node


    def test_get_refresh_master(self,client,get_header,get_mock):
        headers = get_header
        id_master = self.var_mock.ids['id_master']
        endpoint = 'api/master/refresh/{}'.format(id_master)
        res = client.get(endpoint,headers=headers)
        assert res.status_code == 200
        res = json.loads(res.data.decode('utf8'))
        assert res['data']['task_id'] == id_master

    def test_get_refresh_slave(self,client,get_header):
        headers = get_header
        id_cs_slave_node = self.var_mock.ids['id_cs_slave_node']
        endpoint = 'api/slave_node/refresh/{}'.format(id_cs_slave_node)
        res = client.get(endpoint,headers=headers)
        assert res.status_code == 200
        res = json.loads(res.data.decode('utf8'))
        assert res['data']['task_id'] == id_cs_slave_node

    
    def test_refresh(self,client,get_header):
        headers = get_header
        id_master = self.var_mock.ids['id_master']
        data = {"refresh-master": {"tags": {"id_master" : id_master}}}
        res = self.post_data(client,'sendcommand',data,headers)
        assert res.status_code == 200
        res = json.loads(res.data.decode('utf8'))
        assert res['status'] == 'success'

        id_cs_slave_node = self.var_mock.ids['id_cs_slave_node']
        data = {"refresh-slave": {"tags": {"id_slave" : id_cs_slave_node}}}
        res = self.post_data(client,'sendcommand',data,headers)
        assert res.status_code == 200
        res = json.loads(res.data.decode('utf8'))
        assert res['status'] == 'success'


    def test_check_master(self,client,get_header):
        headers = get_header
        res = client.get('api/slave_node',headers=headers)
        res = json.loads(res.data.decode('utf8'))
        data = res['data'][0]
        send_data = {"status_agent":"slave","nm_host":data['nm_slave_node'],"data_zone":""}
        

        res = self.post_data(client,'agent/check',send_data,headers)
        assert res.status_code == 200


        res = client.get('api/master',headers=headers)
        res = json.loads(res.data.decode('utf8'))
        data = res['data'][0]
        send_data = {"status_agent": "master","nm_host": data['nm_master'],"data_zone":""}
        res = self.post_data(client,'agent/check',send_data,headers)
        assert res.status_code == 200

    def test_check_log(self,client,get_header):
        headers = get_header
        res = client.get('api/master',headers=headers)
        res = json.loads(res.data.decode('utf8'))
        data = res['data'][0]
        id_master = data['id_master']
        endpoint = 'api/agent/master/{}'.format(id_master)
        res = client.get(endpoint,headers=headers)
        assert res.status_code == 200

        res = client.get('api/slave_node',headers=headers)
        res = json.loads(res.data.decode('utf8'))
        data = res['data'][0]
        id_slave = data['id_cs_slave_node']
        endpoint = 'api/agent/slave/{}'.format(id_slave)
        res = client.get(endpoint,headers=headers)
        assert res.status_code == 200

        # UNSET CHECK MASTER

        endpoint_unsetmaster = 'api/cluster/unset/master/{}'.format(id_master)
        endpoint_unsetzone = 'api/cluster/unset/slave/{}'.format(id_slave)

        res = client.get(endpoint_unsetmaster,headers=headers)
        assert res.status_code == 200

        res = client.get(endpoint_unsetzone,headers=headers)
        assert res.status_code == 200

