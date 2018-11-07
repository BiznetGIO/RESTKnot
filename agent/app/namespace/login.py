from flask import Flask, session, request
from flask_socketio import Namespace, emit, disconnect
import dill
from command import read_rest
from passlib.hash import pbkdf2_sha256
from app import redis
from flask_jwt_extended import create_access_token


class LoginNamespace(Namespace):
    def on_login(self, data):
        check_user = redis.get(data['username'])
        if not check_user:
            emit('log_response', "User Not Found")
        else:
            users = dill.loads(check_user)
            if pbkdf2_sha256.verify(data['password'], users['password']):
                
                access_token = create_access_token(identity=users['username'])
                data={
                    'token': access_token,
                    'username': session['username']
                }
                sess = dill.dumps(data)
                redis.set(access_token, sess)
                response={
                    'token': access_token,
                    'session': sess,
                    'status': True
                }
                session['username'] = users['username']
                session['token'] = access_token
            else:
                print(False)
            
            emit('log_response', response)
        # disconnect()

    def on_signup(self, data):
        check_data = redis.get(data['username'])
        if check_data:
            emit('log_response', "username Duplicate")
        else:
            password = data['password']
            password_hash = pbkdf2_sha256.hash(password)
            data = {
                "username": data['username'],
                "access": data['access'],
                "password": password_hash
            }
            sess = dill.dumps(data)
            redis.set(data['username'], sess)
            respons = {
                "data":{
                    "username": data['username'],
                    "access": data['access'],
                },
                "status": True,
            }
            emit('log_response', respons)

    def on_disconnect_request(self):
        session['receive_count'] = session.get('receive_count', 0) + 1
        emit('client',
             {'data': 'Disconnected!', 'count': session['receive_count']})
        disconnect()

    def on_connect(self):
        emit('client', {'data': 'Connected', 'client': request.sid})

    def on_disconnect(self):
        print('Client disconnected', request.sid)