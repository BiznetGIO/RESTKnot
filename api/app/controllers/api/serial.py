from flask_restful import Resource, reqparse
from app.helpers.rest import response
from app.models import model
from app.libs import utils
from app.middlewares import auth


def get_datum(data):
    if data is None:
        return

    results = []
    for d in data:
        datum = {
            "id": d["id"],
            "name": d["name"],
            "serial": d["serial"],
            "record_id": d["record_id"],
        }
        results.append(datum)
    return results


class GetSerialData(Resource):
    @auth.auth_required
    def get(self):
        try:
            serials = model.get_all("serial")
        except Exception as e:
            return response(401, message=str(e))
        else:
            data = get_datum(serials)
            return response(200, data=data)


class GetSerialDataId(Resource):
    @auth.auth_required
    def get(self, serial_id):
        try:
            serial = model.get_by_id(table="serial", field="id", id_=serial_id)
        except Exception as e:
            return response(401, message=str(e))
        else:
            data = get_datum(serial)
            return response(200, data=data)


class SerialAdd(Resource):
    @auth.auth_required
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("name", type=str, required=True)
        parser.add_argument("serial", type=str, required=True)
        parser.add_argument("record_id", type=str, required=True)
        args = parser.parse_args()

        name = args["name"]
        serial = args["serial"]
        record_id = args["record_id"]

        # FIXME
        # Check Relation
        # if model.check_relation("zn_record", id_record):
        #     return response(401, message="Relation to Record error Check Your Key")

        # Validation
        if not utils.check_record_serial(record_id):
            return response(401, message="No Serial Record")

        data = {"name": name, "serial": serial, "record_id": record_id}

        try:
            model.insert(table="serial", data=data)
        except Exception as e:
            return response(401, message=str(e))
        else:
            return response(200, data=data, message="Inserted")


class SerialEdit(Resource):
    @auth.auth_required
    def put(self, serial_id):
        parser = reqparse.RequestParser()
        parser.add_argument("serial", type=str, required=True)
        parser.add_argument("name", type=str, required=True)
        parser.add_argument("record_id", type=str, required=True)
        args = parser.parse_args()
        serial = args["serial"]
        name = args["name"]
        record_id = args["record_id"]

        # Check Relation
        # if model.check_relation("record", record_id):
        #     return response(401, message="Relation to Record error Check Your Key")
        # if not utils.check_record_serial(record_id):
        #     return response(401, message="No Serial Record")

        data = {
            "where": {"id": serial_id},
            "data": {"name": name, "serial": serial, "record_id": record_id},
        }
        try:
            model.update("serial", data=data)
        except Exception as e:
            return response(401, message=str(e))
        else:
            return response(200, data=data, message="Edited")


class SerialDelete(Resource):
    @auth.auth_required
    def delete(self, serial_id):
        try:
            data = model.delete(table="serial", field="id", value=serial_id)
        except Exception as e:
            return response(401, message=str(e))
        else:
            return response(200, data=data, message="Deleted")
