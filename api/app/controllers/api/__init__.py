from flask import Blueprint
from flask_restful import Api
from .domain import *
from .record_name import *
from .ttl import *
from .zone import *
from .record_data import *
from .ttl_data import *
from .content import *
from .content_data import *
from .command import *


api_blueprint = Blueprint("api", __name__, url_prefix='/api')
api = Api(api_blueprint)

api.add_resource(DomainCommand, '/domain')
api.add_resource(RecordName, '/namerecord')
api.add_resource(TtlName, '/ttl')
api.add_resource(ZoneName, '/zone')
api.add_resource(RecordData, '/datarecord')
api.add_resource(TtlData, '/datattl')
api.add_resource(ContentName, '/content')
api.add_resource(ContentData, '/datacontent')
api.add_resource(SendCommand, '/sendcommand')