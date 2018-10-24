from flask_restful import Resource, reqparse, request
from app.helpers.rest import *
from app.models import domain_models as dm
from app.helpers import cmd_parser as cmd


class DomainAll(Resource):
    def get(self):
        # status = domain.insert(data={
        #     "domain_name": "rosa.com.",
        # })
        # print(status)

        # status = domain.delete("domain_d0cab4cc907e6b6fe714c7f477644d9b")

        try:
            respons = dm.result()
        except Exception as e:
            respons = None
        else:
            return response(200, data=respons)

class DomainCommand(Resource):
    def post(self):
        json_req = request.get_json(force=True)
        cmd.parser(json_req)

        respons = ""
        return response(200, data=respons)