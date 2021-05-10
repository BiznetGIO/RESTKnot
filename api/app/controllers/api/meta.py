from flask_restful import Resource

from app.vendors.rest import response
from app.helpers import helpers
from app.middlewares import auth


class MetaVersion(Resource):
    def get(self):
        build = helpers.read_version("requirements.txt", "build-version.txt")

        data = {"build": build}
        return response(200, data=data, message="OK")


class MetaConfig(Resource):
    @auth.auth_required
    def get(self):
        config = helpers.get_config()
        brokers = config["brokers"]
        clusters = config["knot_servers"]

        data = {"knot_servers": clusters, "brokers": brokers}
        return response(200, data=data, message="OK")
