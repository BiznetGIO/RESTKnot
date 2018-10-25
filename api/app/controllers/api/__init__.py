from flask import Blueprint
from flask_restful import Api
from .domain import *
from .record_name import *
from .ttl import *

api_blueprint = Blueprint("api", __name__, url_prefix='/api')
api = Api(api_blueprint)

api.add_resource(DomainCommand, '/domain')
api.add_resource(RecordName, '/recordname')
api.add_resource(TtlName, '/ttl')