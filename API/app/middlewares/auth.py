from flask import Flask, jsonify, request
from app.models import model as db
from app.helpers.rest import response
from app import redis_store
from functools import wraps
import os

def check_admin_mode(ip):
    whitelist_ip = os.getenv('ACL')
    admin_ip = whitelist_ip.split(",")
    admin_ip = [i.replace(' ','') for i in admin_ip]
    check_ip = ip in admin_ip
    return check_ip

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'Access-Token' not in request.headers:
            check_admin = check_admin_mode(request.remote_addr)
            if not check_admin:
                return response(400, message="Your not access")
        else:
            access_token = request.headers['Access-Token']
            stored_data = redis_store.get('{}'.format(access_token))
            if not stored_data:
                return response(400, message=" Invalid access token ")

        return f(*args, **kwargs)
    return decorated_function