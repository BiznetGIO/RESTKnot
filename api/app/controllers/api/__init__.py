from flask import Blueprint
from flask_restful import Api
from .domain import *


api_blueprint = Blueprint("api", __name__, url_prefix='/api')
api = Api(api_blueprint)

api.add_resource(DomainAll, '/domain')
api.add_resource(DomainCommand, '/domain')