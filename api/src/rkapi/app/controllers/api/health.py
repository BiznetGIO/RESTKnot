from confluent_kafka import KafkaError, KafkaException
from flask_restful import Resource

from rkapi.app.helpers.producer import kafka_admin
from rkapi.app.vendors.rest import response


class HealthCheck(Resource):
    def get(self):
        data = {"status": "running"}
        return response(200, data=data, message="OK")


class AllHealthCheck(Resource):
    def get(self):
        broker_status = "unknown"

        admin_client = kafka_admin()

        try:
            topics = admin_client.list_topics(timeout=5).topics
            if topics:
                broker_status = "connected"
        except KafkaException as e:
            if e.args[0].code() in (KafkaError._TIMED_OUT, KafkaError._TRANSPORT):
                broker_status = "not connected"

        data = {"status": "running", "broker_status": broker_status}
        return response(200, data=data, message="OK")
