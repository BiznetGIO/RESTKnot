from flask_restful import Resource

from rkapi.app.helpers import helpers
from rkapi.app.middlewares import auth
from rkapi.app.vendors.rest import response


class MetaVersion(Resource):
    def get(self):
        build = helpers.read_version()

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
