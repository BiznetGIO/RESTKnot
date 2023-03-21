# didn't work with apline
FROM python:3.11-slim-buster

ENV PIP_DEFAULT_TIMEOUT=100 \
  POETRY_VERSION=1.4

RUN apt-get update
# working with timezones
RUN apt-get install --no-install-recommends --yes tzdata
# confluent-kafka-python needs these
RUN apt-get install --no-install-recommends --yes gcc librdkafka-dev python3-dev

# activate virtualenv
ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# upgrading pip solves many installation problems
RUN pip3 install --upgrade pip
RUN pip3 install "poetry==$POETRY_VERSION"

WORKDIR /dnsagent

# leverage Docker cache
COPY poetry.lock pyproject.toml /dnsagent/

RUN poetry install --only main --no-interaction --no-ansi

ARG VCS_REVISION
RUN echo "$VCS_REVISION" > version

COPY . /dnsagent

# check build version
RUN cat /dnsagent/version

ENV PYTHONPATH "${PYTHONPATH}:/dnsagent"
CMD ["python3", "dnsagent/start.py"]
