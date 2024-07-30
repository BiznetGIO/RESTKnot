FROM python:3.11.3-slim-buster

RUN apt-get update
# working with timezones
RUN apt-get install --no-install-recommends --yes tzdata
# confluent-kafka-python needs these
RUN apt-get install --no-install-recommends --yes librdkafka-dev python3-dev
# psycopg2 needs these
RUN apt-get install --no-install-recommends --yes build-essential libpq-dev

RUN --mount=source=dist,target=/dist PYTHONDONTWRITEBYTECODE=1 pip install --no-cache-dir /dist/*.whl

ARG VCS_REVISION
RUN echo "$VCS_REVISION" > version

COPY src/rkapi .

EXPOSE 5000
CMD ["gunicorn", "autoapp:app", "-b", "0.0.0.0:5000"]
