from typing import Dict

from flask import Response, current_app
from flask_restful import Resource, reqparse

from app.helpers import command, helpers, producer, rules, validator
from app.helpers.rest import response
from app.middlewares import auth
from app.models import record as record_db
from app.models import ttl as ttl_db
from app.models import type_ as type_db
from app.models import zone as zone_db


def get_soa_record(zone_name) -> Dict:
    soa_record: Dict = {}

    zone = zone_db.get_by_name(zone_name)
    if not zone:
        raise ValueError("zone not found")

    records = record_db.get_by_zone_id(zone["id"])
    if not records:
        raise ValueError("records not found")

    for record in records:
        soa_type = type_db.get_by_value("SOA")
        if not soa_type:
            raise ValueError("type not found")

        soa_type_id = soa_type["id"]
        if record["type_id"] == soa_type_id:
            soa_record = record
            break

    return soa_record


def get_soa_serial(zone_name) -> str:
    soa_record = get_soa_record(zone_name)

    rdatas = soa_record["rdata"].split(" ")
    serial = rdatas[2]

    return serial


def check_serial_limit(serial: str):
    # `serial_counter` is the last two digit of serial value (YYYYMMDDnn)
    serial_counter = serial[-2:]
    serial_date = serial[:-2]

    today_date = helpers.soa_time_set()

    if int(serial_counter) > 97 and serial_date == today_date:
        # knot maximum of nn is 99
        # 97 was chosen because serial
        # increment can be twice at time
        raise ValueError("zone change limit reached")


def update_soa_serial(zone_name: str, increment: str = "01"):
    """Update serial in rdata"""

    soa_record = get_soa_record(zone_name)
    old_serial = get_soa_serial(zone_name)

    _new_serial = helpers.increment_serial(old_serial, increment)
    new_rdata = helpers.replace_serial(soa_record["rdata"], _new_serial)

    record_db.update(
        owner=soa_record["owner"],
        rdata=new_rdata,
        zone_id=soa_record["zone_id"],
        type_id=soa_record["type_id"],
        ttl_id=soa_record["ttl_id"],
        record_id=soa_record["id"],
    )


class GetRecordData(Resource):
    @auth.auth_required
    def get(self) -> Response:
        try:
            records = record_db.get_all()
            if not records:
                return response(404)

            records_detail = []
            for record in records:
                zone = zone_db.get(record["zone_id"])
                if not zone:
                    return response(404, message="zone not found")

                type_ = type_db.get(record["type_id"])
                if not type_:
                    return response(404, message="type not found")

                ttl = ttl_db.get(record["ttl_id"])
                if not ttl:
                    return response(404, message="ttl not found")

                detail = {
                    "id": record["id"],
                    "owner": record["owner"],
                    "rdata": record["rdata"],
                    "zone": zone["zone"],
                    "type": type_["type"],
                    "ttl": ttl["ttl"],
                }
                records_detail.append(detail)

            return response(200, data=records_detail)
        except Exception as e:
            current_app.logger.error(f"{e}")
            return response(500)


class GetRecordDataId(Resource):
    @auth.auth_required
    def get(self, record_id: int) -> Response:
        try:
            record = record_db.get(record_id)
            if not record:
                return response(404)

            zone = zone_db.get(record["zone_id"])
            if not zone:
                return response(404, message="zone not found")

            type_ = type_db.get(record["type_id"])
            if not type_:
                return response(404, message="type not found")

            ttl = ttl_db.get(record["ttl_id"])
            if not ttl:
                return response(404, message="ttl not found")

            detail = {
                "id": record["id"],
                "owner": record["owner"],
                "rdata": record["rdata"],
                "zone": zone["zone"],
                "type": type_["type"],
                "ttl": ttl["ttl"],
            }

            return response(200, data=detail)
        except Exception as e:
            current_app.logger.error(f"{e}")
            return response(500)


class RecordAdd(Resource):
    @producer.check_producer
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
        parser.add_argument("zone", type=str, required=True)
        parser.add_argument("owner", type=str, required=True)
        parser.add_argument("rtype", type=str, required=True)
        parser.add_argument("rdata", type=str, required=True)
        parser.add_argument("ttl", type=str, required=True)
        args = parser.parse_args()
        owner = args["owner"]
        rtype = args["rtype"]
        rdata = args["rdata"]
        zone_name = args["zone"]
        ttl_value = args["ttl"]

        # Validate input
        ttl = ttl_db.get_by_value(ttl_value)
        if not ttl:
            return response(404, message="ttl not found")

        type_ = type_db.get_by_value(rtype)
        if not type_:
            return response(404, message="type not found")

        zone = zone_db.get_by_name(zone_name)
        if not zone:
            return response(404, message="zone not found")

        try:
            rules.check_add(
                rtype=rtype,
                zone_id=zone["id"],
                type_id=type_["id"],
                owner=owner,
                rdata=rdata,
                ttl_id=ttl["id"],
            )

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
            serial = get_soa_serial(zone["zone"])
            check_serial_limit(serial)
        except Exception as e:
            return response(429, message=f"{e}")

        try:
            record = record_db.add(
                owner=owner,
                rdata=rdata,
                zone_id=zone["id"],
                type_id=type_["id"],
                ttl_id=ttl["id"],
            )
            if not record:
                raise ValueError("failed to store record")

            command.set_zone(record["id"], "zone-set")

            # increment serial after adding new record
            if type_["type"] != "SOA":
                update_soa_serial(zone["zone"])

            updated_record = record_db.get(record["id"])
            if not updated_record:
                return response(500, message="failed to update record")

            zone = zone_db.get(updated_record["zone_id"])
            if not zone:
                return response(404, message="zone not found")

            type_ = type_db.get(updated_record["type_id"])
            if not type_:
                return response(404, message="type not found")

            ttl = ttl_db.get(updated_record["ttl_id"])
            if not ttl:
                return response(404, message="ttl not found")

            result = {
                "id": updated_record["id"],
                "owner": updated_record["owner"],
                "rdata": updated_record["rdata"],
                "zone": zone["zone"],
                "type": type_["type"],
                "ttl": ttl["ttl"],
            }
            return response(201, data=result)
        except Exception as e:
            current_app.logger.error(f"{e}")
            return response(500)


class RecordEdit(Resource):
    @producer.check_producer
    @auth.auth_required
    def put(self, record_id: int) -> Response:
        parser = reqparse.RequestParser()
        parser.add_argument("zone", type=str, required=True)
        parser.add_argument("owner", type=str, required=True)
        parser.add_argument("rtype", type=str, required=True)
        parser.add_argument("rdata", type=str, required=True)
        parser.add_argument("ttl", type=str, required=True)
        args = parser.parse_args()
        owner = args["owner"]
        rtype = args["rtype"]
        rdata = args["rdata"]
        zone_name = args["zone"]
        ttl_value = args["ttl"]

        # Validate input
        ttl = ttl_db.get_by_value(ttl_value)
        if not ttl:
            return response(404, message="ttl not found")

        type_ = type_db.get_by_value(rtype)
        if not type_:
            return response(404, message="type not found")

        zone = zone_db.get_by_name(zone_name)
        if not zone:
            return response(404, message="zone not found")

        # Check rules
        try:
            rules.check_edit(
                rtype=rtype,
                zone_id=zone["id"],
                type_id=type_["id"],
                owner=owner,
                rdata=rdata,
                ttl_id=ttl["id"],
                record_id=record_id,
            )
        except Exception as e:
            return response(409, message=f"{e}")

        try:
            validator.validate(rtype, rdata)
            validator.validate("owner", owner)
        except Exception as e:
            return response(422, message=f"{e}")

        try:
            serial = get_soa_serial(zone["zone"])
            check_serial_limit(serial)
        except Exception as e:
            return response(429, message=f"{e}")

        try:
            command.set_zone(record_id, "zone-unset")
            record = record_db.update(
                owner=owner,
                rdata=rdata,
                zone_id=zone["id"],
                type_id=type_["id"],
                ttl_id=ttl["id"],
                record_id=record_id,
            )
            if not record:
                raise ValueError("failed to update record")
            command.set_zone(record_id, "zone-set")

            # increment serial after adding new record
            if type_["type"] != "SOA":
                update_soa_serial(zone["zone"], "02")

            updated_record = record_db.get(record_id)
            if not updated_record:
                return response(404, message="records not found")

            zone = zone_db.get(updated_record["zone_id"])
            if not zone:
                return response(404, message="zone not found")

            type_ = type_db.get(updated_record["type_id"])
            if not type_:
                return response(404, message="type not found")

            ttl = ttl_db.get(updated_record["ttl_id"])
            if not ttl:
                return response(404, message="ttl not found")

            result = {
                "id": updated_record["id"],
                "owner": updated_record["owner"],
                "rdata": updated_record["rdata"],
                "zone": zone["zone"],
                "type": type_["type"],
                "ttl": ttl["ttl"],
            }
            return response(200, data=result)
        except Exception as e:
            current_app.logger.error(f"{e}")
            return response(500)


class RecordDelete(Resource):
    @producer.check_producer
    @auth.auth_required
    def delete(self, record_id: int) -> Response:
        """Delete specific record.

        note:
        SOA record can't be deleted. One zone must have minimum one SOA record at time.
        But it can be edited, see`record edit`.
        """
        record = record_db.get(record_id)
        if not record:
            return response(status_code=404, message="record not found")

        zone = zone_db.get(record["zone_id"])
        if not zone:
            return response(status_code=404, message="zone not found")

        try:
            serial = get_soa_serial(zone["zone"])
            check_serial_limit(serial)
        except Exception as e:
            return response(429, message=f"{e}")

        try:
            type_ = type_db.get(record["type_id"])
            if not type_:
                return response(status_code=404, message="type not found")

            if type_["type"] == "SOA":
                return response(403, message="failed to delete SOA record")
            if type_["type"] != "SOA":
                update_soa_serial(zone["zone"])

            command.set_zone(record_id, "zone-unset")

            record_db.delete(record_id)
            return response(204)
        except Exception as e:
            current_app.logger.error(f"{e}")
            return response(500)
