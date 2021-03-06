from flask_restful import Resource

from app.vendors.rest import response
from app.helpers import helpers


class HealthCheck(Resource):
    def get(self):
        build = helpers.read_version("requirements.txt", "build-version.txt")

        data = {"status": "running", "build": build}
        return response(200, data=data, message="OK")
