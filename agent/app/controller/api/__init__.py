from flask import Blueprint
from flask_restful import Api
from .command_rest import *


api_blueprint = Blueprint("api", __name__, url_prefix='/api')
api = Api(api_blueprint)
api.add_resource(CommandRest, '/command_rest')
api.add_resource(CheckOnServer, '/bootstrap')

