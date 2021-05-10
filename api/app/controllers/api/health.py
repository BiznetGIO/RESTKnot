from flask_restful import Resource

from app.vendors.rest import response


class HealthCheck(Resource):
    def get(self):
        data = {
            "status": "running",
        }
        return response(200, data=data, message="OK")
