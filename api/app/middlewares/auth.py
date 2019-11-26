import os
from flask import request
from app.helpers.rest import response
from functools import wraps


def auth_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user_key = request.headers.get("X-API-Key", None)
        app_key = os.environ.get("RESTKNOT_API_KEY")

        if user_key != app_key:
            return response(400, message="Access denied")

        return f(*args, **kwargs)

    return decorated_function
