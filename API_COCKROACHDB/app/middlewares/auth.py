from app.models import model as db
from app.helpers.rest import response
from app import jwt
from flask_jwt_extended import jwt_required
from flask_jwt_extended import (
                                JWTManager,
                                create_access_token,
                                get_jwt_identity,
                                jwt_refresh_token_required
                               )


@jwt.expired_token_loader
def my_expired_token_callback():
    data = {
        'msg': "The token has expired",
        'sub_status': 42
    }
    return response(401, data=data)


@jwt.user_identity_loader
def user_identity_lookup(user):
    return user['username']


def user_loader(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        username = get_jwt_identity()
        user = db.get_by_id(
                    table= "userlogin", 
                    field="username",
                    value=username
                )
        
        if not user:
            data = {
                        "msg": "user not found"
                    }
            return response(404, data=data)
        g.user = user[0]
        return fn(*args, **kwargs)
    return wrapper
