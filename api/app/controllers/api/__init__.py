from flask import Blueprint
from flask_restful import Api

from .domain import (
    AddDomain,
    DeleteDomain,
    GetDomainByUser,
    GetDomainData,
    GetDomainDataId,
)
from .health import HealthCheck
from .meta import MetaVersion, MetaConfig
from .record import GetRecordData, GetRecordDataId, RecordAdd, RecordDelete, RecordEdit
from .ttl import GetTtlData, GetTtlDataId, TtlAdd, TtlDelete, TtlEdit
from .type_ import GetTypeData, GetTypeDataId, TypeAdd, TypeDelete, TypeEdit
from .user import GetUserData, GetUserDataId, UserDelete, UserSignUp, UserUpdate

api_blueprint = Blueprint("api", __name__, url_prefix="/api")
api = Api(api_blueprint)


api.add_resource(HealthCheck, "/health")
api.add_resource(MetaVersion, "/meta/version")
api.add_resource(MetaConfig, "/meta/config")

api.add_resource(GetRecordData, "/record/list")
api.add_resource(GetRecordDataId, "/record/list/<record_id>")
api.add_resource(RecordAdd, "/record/add")
api.add_resource(RecordEdit, "/record/edit/<record_id>")
api.add_resource(RecordDelete, "/record/delete/<record_id>")

api.add_resource(GetDomainData, "/domain/list")
api.add_resource(GetDomainDataId, "/domain/list/zone/")
api.add_resource(GetDomainByUser, "/domain/list/user/<user_id>")
api.add_resource(DeleteDomain, "/domain/delete")
api.add_resource(AddDomain, "/domain/add")

api.add_resource(UserSignUp, "/user/add")
api.add_resource(GetUserData, "/user/list")
api.add_resource(GetUserDataId, "/user/list/")
api.add_resource(UserUpdate, "/user/edit/<user_id>")
api.add_resource(UserDelete, "/user/delete/<user_id>")

# internal usage (db only, didn't communicate with knot)

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
