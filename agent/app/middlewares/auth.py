from app import jwt, redis
from flask import Flask, session
from flask_socketio import emit
from functools import wraps


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        access_token = session['token']
        stored_data = redis.get('{}'.format(access_token))
        if not stored_data:
            emit('response', "No Auth")
        return f(*args, **kwargs)
    return decorated_function


