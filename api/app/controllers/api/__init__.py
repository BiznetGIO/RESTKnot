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
from .cs_master import *
from .cs_slave_node import *
from .cluster import *
from .check_on import *

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

## CLUSTERING
api.add_resource(CsMaster,'/master')
api.add_resource(CsSlave,'/slave_node')

## CLUSTER
api.add_resource(ClusterCheckMaster, '/cluster/master/<id_master>')
api.add_resource(ClusterCheckSlave, '/cluster/slave/<id_slave>')
api.add_resource(ClusterUnsetCheckMaster, '/cluster/unset/master/<id_master>')
api.add_resource(ClusterUnsetCheckSlave, '/cluster/unset/slave/<id_slave>')

# CHECK ON
api.add_resource(NotifyOnAgent, "/agent/check")
api.add_resource(ChekcLogSyncOnMaster, '/agent/master/<id_logs>')
api.add_resource(CheckLogSyncOnSlave, '/agent/slave/<id_logs>')


