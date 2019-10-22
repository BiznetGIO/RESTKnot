from flask_restful import Resource, reqparse
from app.helpers.rest import response
from app.models import model
from app.libs import utils
from app.libs import validation
from app.middlewares import auth


def get_datum(data):
    if data is None:
        return

    results = []
    for d in data:
        # FIXME add created_at?
        datum = {
            "id": str(d["id"]),
            "record": d["record"],
            "zone_id": d["zone_id"],
            "type_id": d["type_id"],
            "ttl_id": d["ttl_id"],
        }
        results.append(datum)
    return results


class GetRecordData(Resource):
    @auth.auth_required
    def get(self):
        try:
            records = model.get_all("record")
        except Exception as e:
            return response(401, message=str(e))

        results = []
        for record in records:
            zone = model.get_by_id(table="zone", field="id", id_=record["zone_id"])
            ttl = model.get_by_id(table="ttl", field="id", id_=record["ttl_id"])
            type_ = model.get_by_id(table="type", field="id", id_=record["type_id"])

            data = {
                "id": record["id"],
                "record": record["record"],
                "zone": zone,
                "type": type_,
                "ttl": ttl,
            }
            results.append(data)

        return response(200, data=results)


class GetRecordDataId(Resource):
    @auth.auth_required
    def get(self, record_id):
        try:
            # data_record = model.read_by_id("record", key)
            records = model.get_by_id(table="record", field="id", id_=record_id)
        except Exception as e:
            return response(401, message=str(e))
        else:
            data = get_datum(records)
            return response(200, data=data)


class RecordAdd(Resource):
    @auth.auth_required
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("record", type=str, required=True)
        parser.add_argument("is_serial", type=bool, required=True)
        parser.add_argument("zone_id", type=str, required=True)
        parser.add_argument("ttl_id", type=str, required=True)
        parser.add_argument("type_id", type=str, required=True)
        args = parser.parse_args()

        # FIXME fill is_serial automatically based on record
        # FIXME fill type_id automatically based on record
        record = args["record"].lower()
        is_serial = args["is_serial"]
        zone_id = args["zone_id"]
        ttl_id = args["ttl_id"]
        type_id = args["type_id"]

        # FIXME drop this, relation handled automatically by cockroach
        # Check Relation Zone
        if model.check_relation("zone", zone_id):
            return response(401, message="Relation to zone error Check Your Key")
        if model.check_relation("type", type_id):
            return response(401, message="Relation to type error Check Your Key")
        if model.check_relation("ttl", ttl_id):
            return response(401, message="Relation to ttl error Check Your Key")

        # validation
        if validation.record_validation(record):
            return response(401, message="Named Error")
        if validation.count_character(record):
            return response(401, message="Count Character Error")
        if validation.record_cname_duplicate(record, type_id, zone_id):
            return response(401, message="Cname Record Duplicate")
        if validation.record_mx_duplicate(record, type_id, zone_id):
            return response(401, message="MX Record Duplicate")

        data = {
            "record": record,
            "is_serial": is_serial,
            "zone_id": zone_id,
            "type_id": type_id,
            "ttl_id": ttl_id,
        }

        try:
            model.insert(table="record", data=data)
        except Exception as e:
            return response(401, message=str(e))
        else:
            return response(200, data=data, message="Inserted")


class RecordEdit(Resource):
    @auth.auth_required
    def put(self, record_id):
        parser = reqparse.RequestParser()
        parser.add_argument("record", type=str, required=True)
        parser.add_argument("is_serial", type=bool, required=True)
        parser.add_argument("zone_id", type=str, required=True)
        parser.add_argument("ttl_id", type=str, required=True)
        parser.add_argument("type_id", type=str, required=True)
        args = parser.parse_args()

        record = args["record"].lower()
        zone_id = args["zone_id"]
        type_id = args["type_id"]
        ttl_id = args["ttl_id"]
        is_serial = args["is_serial"]

        # Check Relation Zone
        if model.check_relation("zone", zone_id):
            return response(401, message="Relation to zone error Check Your Key")
        if model.check_relation("type", type_id):
            return response(401, message="Relation to type error Check Your Key")
        if model.check_relation("ttl", ttl_id):
            return response(401, message="Relation to ttl error Check Your Key")

        # validation
        if validation.record_validation(record):
            return response(401, message="Named Error")
        if validation.count_character(record):
            return response(401, message="Count Character Error")
        if validation.record_cname_duplicate(record, type_id, zone_id):
            return response(401, message="Cname Record Duplicate")
        if validation.record_mx_duplicate(record, type_id, zone_id):
            return response(401, message="MX Record Duplicate")

        data = {
            "where": {"id": record_id},
            "data": {
                "record": record,
                "is_serial": is_serial,
                "zone_id": zone_id,
                "type_id": type_id,
                "ttl_id": ttl_id,
            },
        }

        try:
            model.update("record", data=data)
        except Exception as e:
            return response(401, message=str(e))
        else:
            return response(200, data=data, message="Edited")


class RecordDelete(Resource):
    @auth.auth_required
    def delete(self, record_id):
        try:
            data = model.delete(table="record", field="id", value=record_id)
        except Exception as e:
            return response(401, message=str(e))
        else:
            return response(200, data=data, message="Deleted")
