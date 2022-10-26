# didn't work with apline
FROM python:3.7-slim-buster

ENV PIP_DEFAULT_TIMEOUT=100 \
  POETRY_VERSION=1.2.2 \
  GUNICORN_VERSION=20.1.0

RUN apt-get update
# working with timezones
RUN apt-get install --no-install-recommends --yes tzdata
# confluent-kafka-python needs these
RUN apt-get install --no-install-recommends --yes librdkafka-dev python3-dev

# upgrading pip solves many installation problems
RUN pip3 install --upgrade pip
RUN pip3 install "poetry==$POETRY_VERSION"

WORKDIR /dnsagent

# leverage Docker cache
COPY poetry.lock pyproject.toml /dnsagent/

RUN poetry config virtualenvs.create false && poetry install --no-dev --no-interaction --no-ansi

ARG BUILD_VERSION
RUN echo "$BUILD_VERSION" > build-version.txt

COPY . /dnsagent

# check build version
RUN cat /dnsagent/build-version.txt

ENV PYTHONPATH "${PYTHONPATH}:/dnsagent"
CMD ["python3", "dnsagent/start.py"]
