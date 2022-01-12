import os
from functools import wraps
from typing import Callable

from flask import request

from app.vendors.rest import response


def auth_required(f: Callable):
    """Decorate given function with authentication check."""

    @wraps(f)
    def decorated_function(*args, **kwargs):
        user_key = request.headers.get("X-API-Key", None)
        app_key = os.environ.get("RESTKNOT_API_KEY")

        if user_key != app_key:
            return response(400, message="Access denied")

        return f(*args, **kwargs)

    return decorated_function
