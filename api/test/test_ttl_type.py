import pytest
import json
import utils

class Mock:
	var_nm = {"nm_ttl" : "1234", "nm_type" : "mock_type"}
	var_id = dict()

class TestTypeTTL:
	mock = Mock()

	def post_data(self,client,endpoint,data,headers):
		url = 'api/'+endpoint
		res = client.post(url,data=json.dumps(data),
					content_type='application/json', headers=headers)
		return res

	def test_insert_type_and_ttl(self,client,get_header):
		header = get_header
		nm_type = self.mock.var_nm['nm_type']
		data = utils.get_model('add',{"nm_type" : nm_type})
		result = self.post_data(client,'type',data=data, headers=header)
		assert result.status_code == 200
		result = json.loads(result.data.decode('utf-8'))
		self.mock.var_id['id_type'] = result['message']['id']
		## INSERT TTL
		header = get_header
		nm_ttl = self.mock.var_nm['nm_ttl']
		data = utils.get_model('add',{'nm_ttl':nm_ttl})
		result =self.post_data(client,'ttl',data=data,headers=header)
		assert result.status_code ==200
		result = json.loads(result.data.decode('utf-8'))
		self.mock.var_id['id_ttl'] = result['message']['id']

		id_list = self.mock.var_id

		for key,value in id_list.items():
			url = key.lstrip("id_")
			send_data = { key : str(value)}
			data = utils.get_model('remove',send_data)
			result = self.post_data(client,url,data,header)
			assert result.status_code == 200
		