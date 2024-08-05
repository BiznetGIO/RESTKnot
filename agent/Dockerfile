# didn't work with apline
FROM python:3.11.3-slim-buster

RUN apt-get update
# working with timezones
RUN apt-get install --no-install-recommends --yes tzdata
# confluent-kafka-python needs these
RUN apt-get install --no-install-recommends --yes gcc librdkafka-dev python3-dev

RUN --mount=source=dist,target=/dist PYTHONDONTWRITEBYTECODE=1 pip install --no-cache-dir /dist/*.whl

CMD ["python3", "-m", "rkagent"]
