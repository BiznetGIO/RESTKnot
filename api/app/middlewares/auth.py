from flask import Flask, request
from app.helpers.rest import response
from functools import wraps
from netaddr import IPNetwork, IPAddress
import os

def check_ip_range(ip, cidr):
    return IPAddress(ip) in IPNetwork(cidr)

def check_admin_mode(ip):
    whitelist_ip = os.environ.get("ACL", os.getenv('ACL','127.0.0.1/24'))
    cidr = whitelist_ip.split(",")
    check_ip = None
    for i in cidr:
        cidr = i.replace(' ','')
        approve_ip = check_ip_range(ip, cidr)
        if approve_ip:
            check_ip = True
            break
    return check_ip

def auth_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        check_admin = check_admin_mode(request.remote_addr)
        if not check_admin:
            return response(400, message="Your not access")
        return f(*args, **kwargs)
    return decorated_function