from flask import Response
from flask_restful import Resource

from app.helpers.rest import response


class HealthCheck(Resource):
    def get(self) -> Response:
        data = {
            "status": "running",
        }
        return response(200, data=data, message="OK")
