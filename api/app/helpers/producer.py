
from app import producer


def send(command):
    try:
        respons = producer.send("domaindata", command)
    except Exception as e:
        raise e
    else:
        respons.get(timeout=60)
        return respons.is_done