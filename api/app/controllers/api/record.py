from flask_restful import Resource, reqparse
from app.helpers.rest import response
from app.models import model
from app.models import zone as zone_model
from app.models import record as record_model
from app.libs import validation
from app.middlewares import auth
from app.helpers import command


def is_duplicate(owner, zone_id):
    query = 'SELECT * FROM "record" WHERE "zone_id"=%(zone_id)s AND "owner"=%(owner)s'
    value = {"zone_id": zone_id, "owner": owner}
    mx_records = model.plain_get(query, value)
    if len(mx_records) >= 1:
        return True

    return False


def get_typeid(record):
    try:
        type_ = model.get_by_condition(table="type", field="type", value=record.upper())
        type_id = type_[0]["id"]
        return type_id
    except Exception:
        return response(401, message="Record Unrecognized")


class GetRecordData(Resource):
    @auth.auth_required
    def get(self):
        try:
            records = model.get_all("record")
            data = record_model.get_other_data(records)
            return response(200, data=data)
        except Exception as e:
            return response(401, message=str(e))


class GetRecordDataId(Resource):
    @auth.auth_required
    def get(self, record_id):
        try:
            records = model.get_by_condition(
                table="record", field="id", value=record_id
            )
            data = record_model.get_other_data(records)
            return response(200, data=data)
        except Exception as e:
            return response(401, message=str(e))


class RecordAdd(Resource):
    @auth.auth_required
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("zone", type=str, required=True)
        parser.add_argument("owner", type=str, required=True)
        parser.add_argument("rtype", type=str, required=True)
        parser.add_argument("rdata", type=str, required=True)
        parser.add_argument("ttl_id", type=str, required=True)
        args = parser.parse_args()
        owner = args["owner"].lower()
        rtype = args["rtype"].lower()
        rdata = args["rdata"]
        zone = args["zone"]
        ttl_id = args["ttl_id"]

        type_id = get_typeid(rtype)

        try:
            zone_id = zone_model.get_zone_id(zone)
        except Exception as e:
            return response(401, message=str(e))

        if validation.record_validation(rtype):
            return response(401, message="Named Error")
        if validation.count_character(rtype):
            return response(401, message="Count Character Error")

        if rtype == "mx" or rtype == "cname":
            if is_duplicate(rtype, zone_id):
                return response(401, message="Duplicate Record found")

        try:
            data = {
                "owner": owner,
                "zone_id": zone_id,
                "type_id": type_id,
                "ttl_id": ttl_id,
            }
            record_id = model.insert(table="record", data=data)

            content_data = {"rdata": rdata, "record_id": record_id}
            model.insert(table="rdata", data=content_data)

            command.send_zone(record_id, "zone-set")
        except Exception as e:
            return response(401, message=str(e))
        else:
            return response(200, data=data, message="Inserted")


class RecordEdit(Resource):
    @auth.auth_required
    def put(self, record_id):
        parser = reqparse.RequestParser()
        parser.add_argument("zone", type=str, required=True)
        parser.add_argument("owner", type=str, required=True)
        parser.add_argument("rtype", type=str, required=True)
        parser.add_argument("rdata", type=str, required=True)
        parser.add_argument("ttl_id", type=str, required=True)
        args = parser.parse_args()
        owner = args["owner"].lower()
        rtype = args["rtype"].lower()
        rdata = args["rdata"]
        zone = args["zone"]
        ttl_id = args["ttl_id"]

        type_id = get_typeid(rtype)

        try:
            zone_id = zone_model.get_zone_id(zone)
        except Exception as e:
            return response(401, message=str(e))

        if validation.record_validation(rtype):
            return response(401, message="Named Error")
        if validation.count_character(rtype):
            return response(401, message="Count Character Error")

        if rtype == "mx" or rtype == "cname":
            if is_duplicate(rtype, zone_id):
                return response(401, message="Duplicate Record found")
        try:
            data = {
                "where": {"id": record_id},
                "data": {
                    "owner": owner,
                    "zone_id": zone_id,
                    "type_id": type_id,
                    "ttl_id": ttl_id,
                },
            }
            content_data = {
                "where": {"record_id": record_id},
                "data": {"rdata": rdata, "record_id": record_id},
            }

            command.send_zone(record_id, "zone-unset")

            model.update("rdata", data=content_data)
            model.update("record", data=data)

            command.send_zone(record_id, "zone-set")

            return response(200, data=data, message="Edited")
        except Exception as e:
            return response(401, message=str(e))


class RecordDelete(Resource):
    @auth.auth_required
    def delete(self, record_id):
        try:
            record = model.get_by_condition(table="record", field="id", value=record_id)
            if not record:
                return response(401, message=f"Record Not Found")

            command.send_zone(record_id, "zone-unset")

            data = model.delete(table="record", field="id", value=record_id)
            return response(200, data=data, message="Deleted")
        except Exception as e:
            return response(401, message=str(e))
