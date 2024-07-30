FROM python:3.11.3-slim-buster

ENV PIP_DEFAULT_TIMEOUT=100 \
    GUNICORN_VERSION=20.1.0

RUN apt-get update
# working with timezones
RUN apt-get install --no-install-recommends --yes tzdata
# confluent-kafka-python needs these
RUN apt-get install --no-install-recommends --yes librdkafka-dev python3-dev
# psycopg2 needs these
RUN apt-get install --no-install-recommends --yes build-essential libpq-dev

# upgrading pip solves many installation problems
RUN pip3 install --upgrade pip
RUN pip3 install "gunicorn==$GUNICORN_VERSION"

WORKDIR /app

# leverage Docker cache
COPY requirements.lock ./
RUN PYTHONDONTWRITEBYTECODE=1 pip install --no-cache-dir -r requirements.lock

COPY config.example.yml ./config.yml

ARG VCS_REVISION
RUN echo "$VCS_REVISION" > ./version

COPY src/rkapi .

EXPOSE 5000
CMD ["gunicorn", "autoapp:app", "-b", "0.0.0.0:5000"]
