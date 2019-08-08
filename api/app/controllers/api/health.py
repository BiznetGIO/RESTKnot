from flask_restful import Resource
from app.helpers.rest import response
from time import sleep

class HealthCheck(Resource):
    def get(self):
        data = {
            "check": "Knot API Ok"
        }
        return response(200, data=data, message="OK")