from flask import current_app
from flask_restful import Resource, reqparse

from app.helpers import command, helpers, rules, validator
from app.middlewares import auth
from app.models import model
from app.models import record as record_model
from app.models import ttl as ttl_model
from app.models import type_ as type_model
from app.models import zone as zone_model
from app.vendors.rest import response


def get_serial_resource(zone):
    soa_record = record_model.get_soa_record(zone)
    if not soa_record:
        raise ValueError("Zone has no SOA record. Any change to the zone is not doable")

    rdata_record = model.get_one(
        table="rdata", field="record_id", value=soa_record["id"]
    )
    rdatas = rdata_record["rdata"].split(" ")
    serial = rdatas[2]
    # `serial_counter` is the last two digit of serial value (YYYYMMDDnn)
    serial_counter = serial[-2:]
    serial_date = serial[:-2]

    return {
        "soa_record": soa_record,
        "rdata_record": rdata_record,
        "serial": serial,
        "serial_counter": serial_counter,
        "serial_date": serial_date,
    }


def check_serial_limit(serial_resource):
    serial_counter = serial_resource["serial_counter"]
    serial_date = serial_resource["serial_date"]
    today_date = helpers.soa_time_set()

    if int(serial_counter) > 97 and serial_date == today_date:
        # knot maximum of nn is 99
        # 97 was chosen because serial
        # increment can be twice at time
        raise ValueError("Zone Change Limit Reached")


def update_serial(serial_resource, increment="01"):
    serial = serial_resource["serial"]
    soa_record = serial_resource["soa_record"]
    rdata_record = serial_resource["rdata_record"]

    new_serial = helpers.increment_serial(serial, increment)
    new_rdata = helpers.replace_serial(rdata_record["rdata"], new_serial)
    content_data = {
        "where": {"record_id": soa_record["id"]},
        "data": {"rdata": new_rdata, "record_id": soa_record["id"]},
    }
    model.update("rdata", data=content_data)


class GetRecordData(Resource):
    @auth.auth_required
    def get(self):
        try:
            records = model.get_all("record")
            if not records:
                return response(404)

            records_detail = []
            for record in records:
                detail = record_model.get_other_data(record)
                records_detail.append(detail)

            return response(200, data=records_detail)
        except Exception as e:
            current_app.logger.error(f"{e}")
            return response(500)


class GetRecordDataId(Resource):
    @auth.auth_required
    def get(self, record_id):
        try:
            record = model.get_one(table="record", field="id", value=record_id)
            if not record:
                return response(404)

            data = record_model.get_other_data(record)
            return response(200, data=data)
        except Exception as e:
            current_app.logger.error(f"{e}")
            return response(500)


class RecordAdd(Resource):
    @helpers.check_producer
    @auth.auth_required
    def post(self):
        """Add new record.

        note:
        Adding any record with other record is allowed. IETF best practice
        is not handled automatically.  Knot didn't handle this too, and let the
        user know the standards themselves.
        See https://tools.ietf.org/html/rfc1912
        """
        parser = reqparse.RequestParser()
        parser.add_argument("zone", type=str, required=True, location="form")
        parser.add_argument("owner", type=str, required=True, location="form")
        parser.add_argument("rtype", type=str, required=True, location="form")
        parser.add_argument("rdata", type=str, required=True, location="form")
        parser.add_argument("ttl", type=str, required=True, location="form")
        args = parser.parse_args()
        owner = args["owner"].lower()
        rtype = args["rtype"].lower()
        rdata = args["rdata"]
        zone = args["zone"]
        ttl = args["ttl"]

        try:
            ttl_id = ttl_model.get_ttlid_by_ttl(ttl)

            type_id = type_model.get_typeid_by_rtype(rtype)
            zone_id = zone_model.get_zone_id(zone)
        except Exception as e:
            return response(404, message=f"{e}")

        try:
            rules.check_add(rtype, zone_id, type_id, owner, rdata, ttl_id)
        except Exception as e:
            return response(409, message=f"{e}")

        try:
            # rtype no need to be validated & no need to check its length
            # `get_typeid` will raise error for non existing rtype
            validator.validate(rtype, rdata)
            validator.validate("owner", owner)
        except Exception as e:
            return response(422, message=f"{e}")

        try:
            serial_resource = get_serial_resource(zone)
            check_serial_limit(serial_resource)
        except Exception as e:
            return response(429, message=f"{e}")

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

            command.set_zone(record_id, "zone-set")

            # increment serial after adding new record
            rtype = type_model.get_type_by_recordid(record_id)
            if rtype != "SOA":
                update_serial(serial_resource)

            record = model.get_one(table="record", field="id", value=record_id)
            data = record_model.get_other_data(record)
            return response(201, data=data)
        except Exception as e:
            current_app.logger.error(f"{e}")
            return response(500)


class RecordEdit(Resource):
    @helpers.check_producer
    @auth.auth_required
    def put(self, record_id):
        parser = reqparse.RequestParser()
        parser.add_argument("zone", type=str, required=True, location="form")
        parser.add_argument("owner", type=str, required=True, location="form")
        parser.add_argument("rtype", type=str, required=True, location="form")
        parser.add_argument("rdata", type=str, required=True, location="form")
        parser.add_argument("ttl", type=str, required=True, location="form")
        args = parser.parse_args()
        owner = args["owner"].lower()
        rtype = args["rtype"].lower()
        rdata = args["rdata"]
        zone = args["zone"]
        ttl = args["ttl"]

        try:
            ttl_id = ttl_model.get_ttlid_by_ttl(ttl)
            record_model.is_exists(record_id)

            type_id = type_model.get_typeid_by_rtype(rtype)
            zone_id = zone_model.get_zone_id(zone)
        except Exception as e:
            return response(404, message=f"{e}")

        try:
            rules.check_edit(rtype, zone_id, type_id, owner, rdata, ttl_id, record_id)
        except Exception as e:
            return response(409, message=f"{e}")

        try:
            validator.validate(rtype, rdata)
            validator.validate("owner", owner)
        except Exception as e:
            return response(422, message=f"{e}")

        try:
            serial_resource = get_serial_resource(zone)
            check_serial_limit(serial_resource)
        except Exception as e:
            return response(429, message=f"{e}")

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

            command.set_zone(record_id, "zone-unset")

            model.update("rdata", data=content_data)
            model.update("record", data=data)

            command.set_zone(record_id, "zone-set")

            # increment serial after adding new record
            rtype = type_model.get_type_by_recordid(record_id)
            if rtype != "SOA":
                update_serial(serial_resource, "02")

            record = model.get_one(table="record", field="id", value=record_id)
            data_ = record_model.get_other_data(record)
            return response(200, data=data_)
        except Exception as e:
            current_app.logger.error(f"{e}")
            return response(500)


class RecordDelete(Resource):
    @helpers.check_producer
    @auth.auth_required
    def delete(self, record_id):
        """Delete specific record.

        note:
        SOA record can't be deleted. One zone must have minimum one SOA record at time.
        But it can be edited, see`record edit`.
        """
        try:
            record_model.is_exists(record_id)
        except Exception:
            return response(404)

        zone = zone_model.get_zone_by_record(record_id)
        zone_name = zone["zone"]

        try:
            serial_resource = get_serial_resource(zone_name)
            check_serial_limit(serial_resource)
        except Exception as e:
            return response(429, message=f"{e}")

        try:
            rtype = type_model.get_type_by_recordid(record_id)
            if rtype == "SOA":
                return response(403, message="Can't Delete SOA Record")
            if rtype != "SOA":
                update_serial(serial_resource)

            command.set_zone(record_id, "zone-unset")

            model.delete(table="record", field="id", value=record_id)
            return response(204)
        except Exception as e:
            current_app.logger.error(f"{e}")
            return response(500)
