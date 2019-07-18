import pytest
import json
import utils


class Vars:
	ids = dict()


class TestCreate:

	var_mock = Vars()

	def post_data(self,client,endpoint,data,headers):
		url = 'api/'+endpoint
		res = client.post(url,data=json.dumps(data),
					content_type='application/json', headers=headers)
		return res
	@pytest.mark.run(order=-1)
	def test_set_default_dns(self,client,get_header,get_mock):

		header = get_header
		nm_zone = get_mock["nm_zone"]

		data = {"domain" : nm_zone}
		result = self.post_data(client,'user/dnscreate',data=data,headers=header)
		assert result.status_code == 200
		result = json.loads(result.data.decode('utf8'))
		print(result)
		id_zone = result['data']['data']['id_zone']
		self.var_mock.ids['id_zone'] = id_zone
		
		#check SOA,NS,and CNAME record
		d_result = list()
		d_idrecord = list()
		data = utils.get_model('where',{"id_zone" : id_zone})

		result = self.post_data(client,'record',data=data,headers=header)
		result = json.loads(result.data.decode('utf8'))
		for i in result['data']:
			d_idrecord.append(i['id_record'])
		
		for i in d_idrecord:
			data = utils.get_model('view',{"id_record" : str(i)})
			result = self.post_data(client,'record',data=data,headers=header)
			result = json.loads(result.data.decode('utf8'))
			d_result.append(result['data'][0]['nm_type'])
		
		assert 'CNAME' in d_result
		assert 'NS'	   in d_result
		assert 'SOA'   in d_result


		## ADD RECORD
		headers = get_header
		id_zone = self.var_mock.ids['id_zone']
		d_list = list()

		# Gather Data

		for key,value in get_mock['requirements'].items():
			id_ttl = utils.get_id('ttl',{"nm_ttl" : value["nm_ttl"]},headers)
			id_ttl = id_ttl[0]
			value.update(id_ttl)
			id_type = utils.get_id('type',{"nm_type" : value["nm_type"]},headers)
			id_type = id_type[0]
			value.update(id_type)
			
			##Posting Records
			reqs = {"nm_record" : value["nm_record"],
							"id_zone"		: str(id_zone),
							"id_type"		: str(value['id_type']),
							"date_record": "2019220207"}


			data = utils.get_model('add',reqs)
			result = self.post_data(client,'record',data,headers)
			result = json.loads(result.data.decode('utf8'))
			id_record = result['message']['id']

			value.update({"id_record" : id_record})

			reqs = {"id_record" : id_record,
							"id_ttl"		: value['id_ttl']}
			data = utils.get_model('add',reqs)
			result = self.post_data(client,'ttldata',data,headers)
			result = json.loads(result.data.decode('utf8'))
			id_ttldata = result['message']['id']

			value.update({"id_ttldata" : id_ttldata})
			reqs = {"id_ttldata" : id_ttldata,
							"nm_content" : value["nm_content"]}
			data = utils.get_model('add',reqs)
			result = self.post_data(client,'content',data,headers)
			result = json.loads(result.data.decode('utf8'))
			id_content = result["message"]["id"]
			value.update({"id_content" : id_content})

			if "nm_content_serial" in value:
				reqs = {"nm_content_serial" : value["nm_content_serial"],
								"id_record"	: id_record}
				data = utils.get_model('add',reqs)
				result = self.post_data(client,'content_serial',data,headers)
				result = json.loads(result.data.decode('utf8'))
				id_content_serial = result["message"]["id"]
				value.update({"id_content_serial" : id_content_serial})
			
			d_list.append(value)

		## Fetch Data from view table and assert

		for row in d_list:
			data = utils.get_model('view',{"id_record" : str(row['id_record'])})
			result = self.post_data(client,'record',data=data,headers=headers)
			assert result.status_code == 200
			result = json.loads(result.data.decode('utf8'))
			result = result['data'][0]
			
			for key,value in result.items():
				if key in row:
					val_1 = row[key].lower()
					val_2 = value.lower()
					print(val_1,val_2)
					assert val_1 == val_2
			

			#Checking Record Content
			data = utils.get_model('view',{"id_record" : str(row['id_record'])})
			res = self.post_data(client,'content',data=data,headers=headers)
			assert res.status_code == 200
			res = json.loads(res.data.decode('utf8'))
			result = dict()
			for i in res['data']:
				if i['id_content'] == row['id_content']:
					result = i

			for key,value in result.items():
				if key in row:
					assert row[key].lower() == value.lower()
			print("ROW : ",row)
			if 'nm_content_serial' in row:
				#Checking Record Content Serial if Exists
				data = utils.get_model('view',{"id_content_serial" : str(row['id_content_serial'])})
				result = self.post_data(client,'content_serial',data=data,headers=headers)
				assert result.status_code == 200
				result = json.loads(result.data.decode('utf8'))
				res = dict()
				for i in result['data']:
					if i['id_content_serial'] == row['id_content_serial']:
						res = i
				
				for key,value in res.items():
					if key in row:
						assert row[key].lower() == value.lower()

			if row['nm_type'].upper() == "SRV":
				data = {"zone-srv-insert":{"tags":{"id_record": row['id_record']}}}
				res = self.post_data(client,'sendcommand',data,headers)
				assert res.status_code == 200
			elif row['nm_type'].upper() == 'MX':
				data = {"zone-mx-insert":{"tags":{"id_record": row['id_record'] }}}
				res = self.post_data(client,'sendcommand',data,headers)
				assert res.status_code == 200
			else :
				data = {"zone-insert":{"tags":{"id_record": row['id_record'] }}}
				res = self.post_data(client,'sendcommand',data,headers)
				assert res.status_code == 200	
		
		self.var_mock.ids.update({"result" : d_list})


		## KNOT TRANSACTION
		id_zone = self.var_mock.ids['id_zone']
		data = {"zone-begin" : {"tags" : {"id_zone" : id_zone}}}
		res = self.post_data(client,"sendcommand",data,get_header)
		assert res.status_code == 200

		data = {"zone-commit" : {"tags" : {"id_zone" : id_zone}}}
		res = self.post_data(client,"sendcommand",data,get_header)
		assert res.status_code == 200

		data = {"conf-read" : {"tags" : ""}}
		res = self.post_data(client,"sendcommand",data,get_header)
		assert res.status_code == 200

	### Testing Content Data Search and View
		d_mock = self.var_mock.ids['result'][0]
		print(d_mock)
		v_end = ['ttldata','record','content','content_serial']
		for key,value in d_mock.items():
			if 'id_' in key:
				url = key.lstrip('id_')
				res = client.get("api/"+url,headers=get_header)
				assert res.status_code
				data = utils.get_model('where',{key : value})
				res = self.post_data(client,url,data,get_header)
				assert res.status_code == 200

				if url in v_end:
					data = utils.get_model("view",{key : ""})
					res = self.post_data(client,url,data,get_header)
					assert res.status_code == 200


					data = utils.get_model("view",{"id_record" : d_mock["id_record"]})
					res = self.post_data(client,url,data,get_header)
					assert res.status_code == 200


