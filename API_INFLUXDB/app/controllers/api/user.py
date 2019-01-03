from flask_restful import Resource, reqparse, fields, request
from app.helpers.rest import *
from app.middlewares.auth import jwt_required
from flask_jwt_extended import (
                                JWTManager,
                                create_access_token,
                                get_jwt_identity,
                                jwt_refresh_token_required
                               )
import datetime
from passlib.hash import pbkdf2_sha256
from app.models import api_models as db
from app.helpers import cmd_parser as cmd
from app.libs import utils


class UserCommand(Resource):
    def get(self):
        command = utils.get_command(request.path)
        resp = []
        try:
            respons = db.result(command)
        except Exception:
            respons = None
        else:
            for i in respons['data']:
                data = {
                    "username": i['username'],
                    "full_name": i['full_name']
                }
                resp.append(data)
            respons['data'] = resp
            return response(200, data=respons)


    def post(self):
        json_req = request.get_json(force=True)
        command = utils.get_command(request.path)
        init_data = cmd.parser(json_req, command)
        respons = dict()
        if init_data['action'] == 'insert':
            password = init_data['data'][0]['fields']['password']
            password_hash = pbkdf2_sha256.hash(password)
            init_data['data'][0]['fields']['password'] = password_hash
            row = utils.check_row(init_data['data'])
            if row:
                respons = db.insert(init_data['data'])
                return response(200, data=respons)
            else:
                return response(200, message="Duplicate "+command)
        elif init_data['action'] == 'where':
            measurement = ""
            tags = dict()
            for i in init_data['data']:
                measurement = i['measurement']
                tags = i['tags']
            respons = db.row(measurement,tags)
            return response(200, data=respons)
        elif init_data['action'] == 'remove':
            measurement = ""
            tags = dict()
            for i in init_data['data']:
                measurement = i['measurement']
                tags = i['tags']
            respons = db.delete(measurement,tags)
            return response(200, data=respons)