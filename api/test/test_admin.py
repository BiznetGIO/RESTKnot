import pytest
import json
import utils
from utils import post_data
import os

class Vars:
    ids = dict()



class TestZone:
    
    var_mock = Vars()

    def post_data(self,client,endpoint,data):
        url = 'api/'+endpoint
        res = client.post(url,data=json.dumps(data),
                    content_type='application/json')
        return res

    @pytest.mark.run(order=1)
    def test_admin_login(self,client,get_creds,get_fail_creds):
        """ Before you begin this test, Set the environment on app/controllers/api/admin/auth.py as follows:
        'ADMIN_USER' = your username, 'ADMIN_PASSWORD' = your password. """
        
        os.environ['ADMIN_USER'] = get_creds['username']
        os.environ['ADMIN_PASSWORD'] = get_creds['password']
        
        datacreds = {
        "project_id": os.getenv('CREDENTIAL_PROJECT_ID'),
        "user_id": os.getenv('CREDENTIAL_USER_ID')
        }
        json_data = json.dumps(datacreds)
        result = client.post('api/user',data=json_data,content_type='application/json')
        ### SUCCESS

        data = {
        "username" : get_creds['username'],
        "password" : get_creds['password'],
        "project_id": get_creds['project_id']
        }
        result = self.post_data(client,"admin/login",data)
        assert result.status_code == 200

        ### FAIL, WRONG PASSWORD

        data = {
        "username" : get_creds['username'],
        "password" : get_fail_creds['password'],
        "project_id": get_fail_creds['project_id']
        }
        result = self.post_data(client,"admin/login",data)
        assert result.status_code == 200

        ### FAIL, PROJECT ID DOESNT EXIST

        data = {
        "username" : get_creds['username'],
        "password" : get_creds['password'],
        "project_id": get_fail_creds['project_id']
        }
        result = self.post_data(client,"admin/login",data)
        assert result.status_code == 200
        
        os.environ.pop("ADMIN_USER")
        os.environ.pop("ADMIN_PASSWORD")

    @pytest.mark.run(order=2)
    def test_get_zone(self,client,get_mock):
    
        
        result = client.get('api/zone')
        assert result.status_code == 200


        ## Check without authorization
        header = {"Access-Token" : "aa"}
        result = client.get('api/zone')
        assert result.status_code == 200

    @pytest.mark.run(order=3)
    def test_insert_zone(self,client,get_mock):

        nm_zone = get_mock['nm_zone']
        
        
        data = utils.get_model('add',{"nm_zone" : nm_zone})
        result = self.post_data(client,'zone',data=data)

        assert result.status_code == 200

        ## Failure
        data = utils.get_model('add',{"nm_zone" : 123})
        result = self.post_data(client,'zone',data=data)
        assert result.status_code == 200


    @pytest.mark.run(order=4)
    def test_search_zone(self,client,get_mock):

        nm_zone = get_mock['nm_zone']
        

        data = utils.get_model('where',{"nm_zone" : nm_zone})
        result = self.post_data(client,'zone',data=data)
        assert result.status_code == 200

        result = json.loads(result.data.decode('utf8'))
        self.var_mock.ids['id_zone'] = result['data'][0]['id_zone']

        data = utils.get_model('where',{"nm_zone" : list()})
        result = self.post_data(client,'zone',data=data)

        assert result.status_code == 200

    @pytest.mark.run(order=5)
    def test_sync_zone(self,client,get_mock):
        
        id_zone = self.var_mock.ids['id_zone']
        data = {'conf-insert': {'tags': {'id_zone': id_zone}}}
        result = self.post_data(client,'sendcommand',data=data)
        assert result.status_code == 200

    @pytest.mark.run(order=6)
    def test_where_ttl(self,client,get_mock):
        nm_ttl = get_mock['nm_ttl']
        data = utils.get_model('where',{"nm_ttl" : nm_ttl})
        result = self.post_data(client,'ttl',data=data)
        assert result.status_code == 200

        result = json.loads(result.data.decode('utf8'))
        id_ttl = result['data'][0]['id_ttl']
        self.var_mock.ids['id_ttl'] = id_ttl

    @pytest.mark.run(order=7)
    def test_where_type(self,client,get_mock):
        
        nm_type = get_mock['nm_type']
        data = utils.get_model('where',{"nm_type" : nm_type})
        result = self.post_data(client,'type',data=data)
        assert result.status_code == 200

        result = json.loads(result.data.decode('utf8'))
        id_type = result['data'][0]['id_type']
        self.var_mock.ids['id_type'] = id_type

    @pytest.mark.run(order=8)
    def test_add_record(self,client):
        
        id_zone = self.var_mock.ids['id_zone']
        id_type = self.var_mock.ids['id_type']
        data = utils.get_model('add',{"nm_record" : "soatest", "date_record" : "2018090909",
                                "id_zone" : str(id_zone), "id_type" : str(id_type)})
        
        result = self.post_data(client,'record',data=data)
        assert result.status_code == 200

        result = json.loads(result.data.decode('utf8'))
        id_record = result["message"]["id"]
        self.var_mock.ids['id_record'] = id_record

    @pytest.mark.run(order=9)
    def test_add_ttldata(self,client):
        
        id_record = self.var_mock.ids['id_record']
        id_ttl = self.var_mock.ids['id_ttl']

        data = utils.get_model('add',{"id_record" : id_record , "id_ttl" : id_ttl})

        result = self.post_data(client,'ttldata',data=data)
        assert result.status_code == 200

        result = json.loads(result.data.decode('utf8'))
        self.var_mock.ids['id_ttldata'] = result['message']['id']

    @pytest.mark.run(order=10)
    def test_add_content(self,client):
        id_ttldata = self.var_mock.ids['id_ttldata']
        

        data = utils.get_model('add',{"id_ttldata" : id_ttldata, "nm_content" : "soacontent"})
        result = self.post_data(client,'content',data=data)
        assert result.status_code == 200

    @pytest.mark.run(order=11)
    def test_add_content_serial(self,client):
        id_record = self.var_mock.ids['id_record']
        
        content_serial = 'test_content_serial'

        data = utils.get_model('add',{"id_record" : id_record, "nm_content_serial" : content_serial})
        result = self.post_data(client,'content_serial',data=data)
        assert result.status_code == 200
    
    @pytest.mark.run(order=12)
    def test_add_remove_zone(self,client):
        id_zone = self.var_mock.ids['id_zone']
        

        data = utils.get_model('remove', {"id_zone" : id_zone})
        result = self.post_data(client,'zone',data=data)
        assert result.status_code == 200

class TestCreate:

	var_mock = Vars()

	def post_data(self,client,endpoint,data,headers=None):
		url = 'api/'+endpoint
		res = client.post(url,data=json.dumps(data),
					content_type='application/json')
		return res

	@pytest.mark.run(order=1)
	def test_set_default_dns(self,client,get_creds,get_mock):

		nm_zone = get_mock["nm_zone"]
		project_id = get_creds['project_id']
		data = {"domain" : nm_zone, "project_id" : project_id}
		result = self.post_data(client,'admin/dnscreate',data=data)
		assert result.status_code == 200
		result = json.loads(result.data.decode('utf8'))
		id_zone = result['data']['data']['id_zone']
		self.var_mock.ids['id_zone'] = id_zone
		
		#check SOA,NS,and CNAME record
		d_result = list()
		d_idrecord = list()
		data = utils.get_model('where',{"id_zone" : id_zone})

		result = self.post_data(client,'record',data=data)
		result = json.loads(result.data.decode('utf8'))
		for i in result['data']:
			d_idrecord.append(i['id_record'])
		
		for i in d_idrecord:
			data = utils.get_model('view',{"id_record" : str(i)})
			result = self.post_data(client,'record',data=data)
			result = json.loads(result.data.decode('utf8'))
			d_result.append(result['data'][0]['nm_type'])
		
		assert 'CNAME' in d_result
		assert 'NS'	   in d_result
		assert 'SOA'   in d_result

	@pytest.mark.run(order=11)
	def test_add_remove_zone(self,client):
		id_zone = self.var_mock.ids['id_zone']
		data = utils.get_model('remove', {"id_zone" : id_zone})
		result = self.post_data(client,'zone',data=data)
		assert result.status_code == 200

