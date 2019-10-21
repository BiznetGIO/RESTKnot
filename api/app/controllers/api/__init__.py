from flask import Blueprint
from flask_restful import Api
from .health import *
from .user import *
from .ttl import *
from .type import *
from .zone import *
from .record import *
from .content import *
from .serial import *
from .domain import *

api_blueprint = Blueprint("api", __name__, url_prefix="/api")
api = Api(api_blueprint)

api.add_resource(HealthCheck, "/health")

api.add_resource(UserSignUp, "/user/add")
api.add_resource(GetUserData, "/user/list")
api.add_resource(GetUserDataId, "/user/list/<user_id>")
api.add_resource(UserUpdate, "/user/edit/<user_id>")
api.add_resource(UserDelete, "/user/delete/<user_id>")

api.add_resource(GetTtlData, "/ttl/list")
api.add_resource(GetTtlDataId, "/ttl/list/<ttl_id>")
api.add_resource(TtlAdd, "/ttl/add")
api.add_resource(TtlEdit, "/ttl/edit/<ttl_id>")
api.add_resource(TtlDelete, "/ttl/delete/<ttl_id>")

api.add_resource(GetTypeData, "/type/list")
api.add_resource(GetTypeDataId, "/type/list/<type_id>")
api.add_resource(TypeAdd, "/type/add")
api.add_resource(TypeEdit, "/type/edit/<type_id>")
api.add_resource(TypeDelete, "/type/delete/<type_id>")

api.add_resource(GetZoneData, "/zone/list")
api.add_resource(GetZoneDataId, "/zone/list/<zone_id>")
api.add_resource(ZoneAdd, "/zone/add")
api.add_resource(ZoneEdit, "/zone/edit/<zone_id>")
api.add_resource(ZoneDelete, "/zone/delete/<zone_id>")

api.add_resource(GetRecordData, "/record/list")
api.add_resource(GetRecordDataId, "/record/list/<record_id>")
api.add_resource(RecordAdd, "/record/add")
api.add_resource(RecordEdit, "/record/edit/<record_id>")
api.add_resource(RecordDelete, "/record/delete/<record_id>")

api.add_resource(GetContentData, "/content/list")
api.add_resource(GetContentDataId, "/content/list/<key>")
api.add_resource(ContentAdd, "/content/add")
api.add_resource(ContentEdit, "/content/edit/<key>")
api.add_resource(ContentDelete, "/content/delete/<key>")

api.add_resource(GetSerialData, "/serial/list")
api.add_resource(GetSerialDataId, "/serial/list/<serial_id>")
api.add_resource(SerialAdd, "/serial/add")
api.add_resource(SerialEdit, "/serial/edit/<serial_id>")
api.add_resource(SerialDelete, "/serial/delete/<serial_id>")

api.add_resource(GetDomainData, "/domain/list")
api.add_resource(GetDomainDataId, "/domain/list/zone/<key>")
api.add_resource(GetDomainDataByProjectId, "/domain/list/user/<project_id>")
api.add_resource(DeleteDomain, "/domain/delete/zone/<key>")
api.add_resource(AddDomain, "/domain/add")


api.add_resource(ViewCommand, "/domain/view/<key>")
