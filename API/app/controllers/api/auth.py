from flask_restful import Resource, reqparse, fields
from app.helpers.rest import response
from app.libs import login_utils
from app.models import model as db
from app import redis_store
import arrow
import hashlib
import uuid
import datetime
import dill
import os

GLOBAL_AUTH_URL = 'https://keystone.wjv-1.neo.id:443/v3'
GLOBAL_USER_DOMAIN_NAME = 'neo.id'


class Usersignin(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', type=str, required=True)
        parser.add_argument('password', type=str, required=True)

        args = parser.parse_args()

        username = args['username']
        password = args['password']

        try:
            sess = login_utils.generate_session(username, password, GLOBAL_AUTH_URL, GLOBAL_USER_DOMAIN_NAME)
        except Exception as e:
            return str(e)
        else:

            user_id = sess.get_user_id()
            project_id = login_utils.get_project_id(sess)
            stored_data = {
                'username': username,
                'user_id':user_id,
                'project_id': project_id,
                'timestamp': arrow.now(),
                'session': sess
            }

            random_string = uuid.uuid4()
            raw_token = '{}{}'.format(random_string, username)
            access_token = hashlib.sha256(raw_token.encode(
                'utf-8')).hexdigest()
            
            try:
                dill_object = dill.dumps(stored_data)
                redis_store.set(access_token, dill_object)
                redis_store.expire(access_token,3600)
            except Exception as e:
                resp = {
                    "error": str(e)
                }
                return response(200, message= resp)
            else:
                data = {
                    "user_id" : user_id,
                    "project_id": project_id,
                    "token": access_token
                }
                return response(200, data= data)


