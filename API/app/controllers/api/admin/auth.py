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


class AdminAuth(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', type=str, required=True)
        parser.add_argument('password', type=str, required=True)
        parser.add_argument('project_id', type=str, required=True)

        args = parser.parse_args()

        username = args['username']
        password = args['password']
        project_id = args['project_id']

        os_admin = os.environ.get("ADMIN_USER", os.getenv('ADMIN_USER'))
        os_password = os.environ.get("ADMIN_PASSWORD", os.getenv('ADMIN_PASSWORD'))

        if username == os_admin and os_password==password:
            data_user = db.get_by_id("userdata", "project_id", project_id)
            if not data_user:
                return response(200, message= "Project ID Not Found")

            stored_data = {
                'username': username,
                'project_id': data_user[0]['project_id'],
                'user_id': data_user[0]['user_id'],
                'timestamp': arrow.now(),
                'session': "admin"
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
                return response(401, message= resp)
            else:
                data = {
                    'project_id': data_user[0]['project_id'],
                    'user_id': data_user[0]['user_id'],
                    "token": access_token
                }
                return response(200, data= data)
        else:
            return response(401, message= "Not Found")


