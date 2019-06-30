from flask import Blueprint
from flask_restful import Api
from .user import *
from .auth import *
from .zone import *
from .type import *
from .ttl import *
from .record import *
from .ttldata import *
from .content import *
from .content_serial import *
from .dns.create import *
from .command_rest import *
from .admin.auth import *
from .admin.create import *

api_blueprint = Blueprint("api", __name__, url_prefix='/api')

api = Api(api_blueprint)

api.add_resource(UserdataResource, '/user')
api.add_resource(UserdataResourceById, '/user/<userdata_id>')
api.add_resource(UserdataInsert, '/user')
api.add_resource(UserdataUpdate, '/user/<userdata_id>')
api.add_resource(UserdataResourceByProjectId, '/user/project/<project_id>')
api.add_resource(UserdataResourceByUserId, '/user/id/<user_id>')
api.add_resource(UserdataRemove, '/user/<userdata_id>')
api.add_resource(Usersignin,"/login")
api.add_resource(UserDataZoneInsert,"/userzone")
api.add_resource(UserDataZoneResource,"/userzone")

## CONF API
api.add_resource(Slave,"/slave")
api.add_resource(SlaveNotify,"/notify_slave")
api.add_resource(SlaveACL,"/acl_slave")
api.add_resource(MasterData,"/master")
api.add_resource(MasterNotify,"/notify_master")
api.add_resource(MasterACL,"/acl_master")

## DNS API
api.add_resource(ZoneName, '/zone')
api.add_resource(Type, '/type')
api.add_resource(TtlName, '/ttl')
api.add_resource(Record, '/record')
api.add_resource(TtlData, '/ttldata')
api.add_resource(Content, '/content')
api.add_resource(ContentSerial, '/content_serial')
api.add_resource(SendCommandRest, '/sendcommand')
api.add_resource(CreateDNS, '/user/dnscreate')

## ADMIN AUTH
api.add_resource(AdminAuth, '/admin/login')
api.add_resource(CreateDNSAdminRole, '/admin/dnscreate')


