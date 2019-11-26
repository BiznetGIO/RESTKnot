from flask_restful import Resource, reqparse
from app.helpers.rest import response
from app.models import model
from app.libs import validation
from app.middlewares import auth


def get_datum(data):
    if data is None:
        return

    results = []
    for d in data:
        datum = {"id": d["id"], "content": d["content"], "record_id": d["record_id"]}
        results.append(datum)
    return results


class GetContentData(Resource):
    @auth.auth_required
    def get(self):
        try:
            contents = model.get_all("content")
        except Exception as e:
            return response(401, message=str(e))
        else:
            data = get_datum(contents)
            return response(200, data=data)


class GetContentDataId(Resource):
    @auth.auth_required
    def get(self, content_id):
        try:
            content = model.get_by_id(table="content", field="id", id_=content_id)
        except Exception as e:
            return response(401, message=str(e))
        else:
            data = get_datum(content)
            return response(200, data=data)


class ContentAdd(Resource):
    @auth.auth_required
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("content", type=str, required=True)
        parser.add_argument("record_id", type=str, required=True)
        args = parser.parse_args()
        content = args["content"].lower()
        record_id = args["record_id"]

        # Validation
        if validation.content_validation(record_id, content):
            return response(401, message="Named Error")
        if validation.count_character(content):
            return response(401, message="Count Character Error")

        data = {"content": content, "record_id": record_id}
        try:
            model.insert(table="content", data=data)
        except Exception as e:
            return response(401, message=str(e))
        else:
            return response(200, data=data, message="Inserted")


class ContentEdit(Resource):
    @auth.auth_required
    def put(self, content_id):
        parser = reqparse.RequestParser()
        parser.add_argument("content", type=str, required=True)
        parser.add_argument("record_id", type=str, required=True)
        args = parser.parse_args()
        content = args["content"].lower()
        record_id = args["record_id"]

        # Validation
        if validation.content_validation(record_id, content):
            return response(401, message="Named Error")
        if validation.count_character(content):
            return response(401, message="Count Character Error")

        data = {
            "where": {"id": content_id},
            "data": {"content": content, "record_id": record_id},
        }
        try:
            model.update("content", data=data)
        except Exception as e:
            return response(401, message=str(e))
        else:
            return response(200, data=data, message="Edited")


class ContentDelete(Resource):
    @auth.auth_required
    def delete(self, content_id):
        try:
            data = model.delete(table="content", field="id", value=content_id)
        except Exception as e:
            return response(401, message=str(e))
        else:
            return response(200, data=data, message="Deleted")
