from flask import Flask, session, request
from flask_socketio import Namespace, emit, disconnect
from app import redis_store
import dill
from command import read_rest
from passlib.hash import pbkdf2_sha256


class LoginNamespace(Namespace):
    def on_login(self, data):
        
        response={
            'data' : "tes",
            "code": 200
        }
        emit('response', response)
        # disconnect()

    def on_signup(self, data):
        
        password = "ocha_ocha"
        password_hash = pbkdf2_sha256.hash(password)
        data = {
            "username":"username",
            "password": password_hash,
            "access": "admin"
        }
        dill_object = dill.dumps(data)
        redis_store.set(access_token, dill_object)

        response={
            'data' : "tes",
            "code": 200
        }
        emit('response',response)


    def on_disconnect_request(self):
        session['receive_count'] = session.get('receive_count', 0) + 1
        emit('client',
             {'data': 'Disconnected!', 'count': session['receive_count']})
        disconnect()

    def on_connect(self):
        emit('client', {'data': 'Connected', 'client': request.sid})

    def on_disconnect(self):
        print('Client disconnected', request.sid)