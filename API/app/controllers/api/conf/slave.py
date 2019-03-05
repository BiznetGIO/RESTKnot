from flask_restful import Resource, reqparse, request
from app.helpers.rest import response
from app.helpers import cmd_parser as cmd
from app.libs import utils
from app.models import model as db
import os
from app.middlewares.auth import login_required


@login_required
class Slave(Resource):
	def get(self):
		command = utils.get_command(request.path)
		command = "cs_"+command
		try:
			results = db.get_all(command)
			obj_userdata = list()
			for i in results :
				data = {
					"id_slave": str(i['id_slave']),
					"nm_slave": i['nm_slave'],
					"ip_slave": i['ip_slave'],
					"port": i['port']
				}
				obj_userdata.append(data)
		except Exception:
			results = None
		else:
			return response(200, data=obj_userdata)

	def post(self):
		json_req = request.get_json(force=True)
		command = utils.get_command(request.path)
		command = "cs_"+command
		init_data = cmd.parser(json_req,command)
		respons = dict()
		if init_data['action'] == 'insert':
			table = init_data['data'][0]['table']
			fields = init_data['data'][0]['fields']
			try:
				result = db.insert(table,fields)
			except Exception as e:
				respons = {
					"status" : False,
					"error"	 : str(e)
				}
			else:
				respons = {
					"status": True,
					"messages": "Fine!",
					"id": result
				}
			finally:
				return response(200,data=fields,message=respons)

		if init_data['action'] == 'where':
			obj_userdata = list()
			table = ""
			fields = ""
			tags = dict()
			for i in init_data['data']:
				table = i['table']
				tags = i['tags']
				for a in tags:
					if tags[a] is not None:
						fields = a
			try:
				result = db.get_by_id(table,fields,tags[fields])
			
			except Exception as e:
				respons = {
					"status" : False,
					"messages": str(e)
				}
			else:
				for i in result:
					data = {
						"id_slave": str(i['id_slave']),
						"nm_slave": i['nm_slave'],
						"ip_slave": str(i['ip_slave']),
						"port":	str(i['port'])
					}
					obj_userdata.append(data)
				respons = {
					"status": True,
					"messages": "Success"
				}
			finally:
				return response(200,data=obj_userdata, message=respons)
			
		if init_data['action'] == 'remove':
			table = ""
			tags = dict()
			fields = ""
			for i in init_data['data']:
				table = i['table']
				tags = i['tags']
			fields = str(list(tags.keys())[0])
			if not isinstance(tags[fields],str) :
				tags[fields] = str(tags[fields])
			try:
				result = db.delete(table,fields,tags[fields])
			except Exception as e:
				respons = {
					"status": False,
					"messages": str(e)
				}
			else:
				respons = {
					"status": result,
					"messages": "data is removed"
				}
			finally:
				return response(200,data=tags,message=respons)

@login_required
class SlaveNotify(Resource):
	def get(self):
		command = utils.get_command(request.path)
		command = "cs_"+command
		try:
			results = db.get_all(command)
			obj_userdata = list()
			for i in results :
				data = {
					"id_slave": str(i['id_slave']),
					"id_notify_master": str(i['id_notify_master']),
					"id_notify_slave": str(i['id_notify_slave'])
				}
				obj_userdata.append(data)
		except Exception:
			results = None
		else:
			return response(200, data=obj_userdata)

	def post(self):
		json_req = request.get_json(force=True)
		command = utils.get_command(request.path)
		command = "cs_"+command
		init_data = cmd.parser(json_req,command)
		respons = dict()
		if init_data['action'] == 'insert':
			table = init_data['data'][0]['table']
			fields = init_data['data'][0]['fields']
			try:
				result = db.insert(table,fields)
			except Exception as e:
				respons = {
					"status" : False,
					"error"	 : str(e)
				}
			else:
				respons = {
					"status": True,
					"messages": "Fine!",
					"id": result
				}
			finally:
				return response(200,data=fields,message=respons)

		if init_data['action'] == 'where':
			obj_userdata = list()
			table = ""
			fields = ""
			tags = dict()
			for i in init_data['data']:
				table = i['table']
				tags = i['tags']
				for a in tags:
					if tags[a] is not None:
						fields = a
			try:
				result = db.get_by_id(table,fields,tags[fields])
			
			except Exception as e:
				respons = {
					"status" : False,
					"messages": str(e)
				}
			else:
				for i in result:
					data = {
					"id_slave": str(i['id_slave']),
					"id_notify_master": str(i['id_notify_master']),
					"id_notify_slave": str(i['id_notify_slave'])
					}
					obj_userdata.append(data)
				respons = {
					"status": True,
					"messages": "Success"
				}
			finally:
				return response(200,data=obj_userdata, message=respons)
			
		if init_data['action'] == 'remove':
			table = ""
			tags = dict()
			fields = ""
			for i in init_data['data']:
				table = i['table']
				tags = i['tags']
			fields = str(list(tags.keys())[0])
			try:
				result = db.delete(table,fields,tags[fields])
			except Exception as e:
				respons = {
					"status": False,
					"messages": str(e)
				}
			else:
				respons = {
					"status": result,
					"messages": "data is removed"
				}
			finally:
				return response(200,data=tags,message=respons)


@login_required
class SlaveACL(Resource):
	def get(self):
		command = utils.get_command(request.path)
		command = "cs_"+command
		try:
			results = db.get_all(command)
			obj_userdata = list()
			for i in results :
				data = {
					"id_acl_slave": str(i['id_acl_slave']),
					"id_acl_master": str(i['id_acl_master']),
					"id_slave": str(i['id_slave'])
				}
				obj_userdata.append(data)
		except Exception:
			results = None
		else:
			return response(200, data=obj_userdata)

	def post(self):
		
		json_req = request.get_json(force=True)
		command = utils.get_command(request.path)
		command = "cs_"+command
		init_data = cmd.parser(json_req,command)
		respons = dict()
		if init_data['action'] == 'insert':
			table = init_data['data'][0]['table']
			fields = init_data['data'][0]['fields']
			try:
				result = db.insert(table,fields)
			except Exception as e:
				respons = {
					"status" : False,
					"error"	 : str(e)
				}
			else:
				respons = {
					"status": True,
					"messages": "Fine!",
					"id": result
				}
			finally:
				return response(200,data=fields,message=respons)

		if init_data['action'] == 'where':
			obj_userdata = list()
			table = ""
			fields = ""
			tags = dict()
			for i in init_data['data']:
				table = i['table']
				tags = i['tags']
				for a in tags:
					if tags[a] is not None:
						fields = a
			try:
				result = db.get_by_id(table,fields,tags[fields])
			
			except Exception as e:
				respons = {
					"status" : False,
					"messages": str(e)
				}
			else:
				for i in result:
					data = {
					"id_acl_slave": str(i['id_acl_slave']),
					"id_acl_master": str(i['id_acl_master']),
					"id_slave": str(i['id_slave'])
					}
					obj_userdata.append(data)
				respons = {
					"status": True,
					"messages": "Success"
				}
			finally:
				return response(200,data=obj_userdata, message=respons)
		
		if init_data['action'] == 'remove':
			table = ""
			tags = dict()
			fields = ""
			for i in init_data['data']:
				table = i['table']
				tags = i['tags']
			fields = str(list(tags.keys())[0])
			try:
				result = db.delete(table,fields,tags[fields])
			except Exception as e:
				respons = {
					"status": False,
					"messages": str(e)
				}
			else:
				respons = {
					"status": result,
					"messages": "data is removed"
				}
			finally:
				return response(200,data=tags,message=respons)