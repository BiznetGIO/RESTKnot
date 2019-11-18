from kafka import KafkaConsumer
from json import loads


def get_kafka_consumer(broker, topic, group_id):
    try:
        consumer = KafkaConsumer(
            topic,
            bootstrap_servers=[broker],
            # auto_offset_reset="earliest",
            # group_id='my-group',
            # enable_auto_commit=True,
            value_deserializer=lambda x: loads(x.decode("utf-8")),
        )
        return consumer
    except Exception as e:
        raise ValueError(e)
