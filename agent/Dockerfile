# didn't work with apline
FROM python:3.11.3-slim-buster

ENV PIP_DEFAULT_TIMEOUT=100

RUN apt-get update
# working with timezones
RUN apt-get install --no-install-recommends --yes tzdata
# confluent-kafka-python needs these
RUN apt-get install --no-install-recommends --yes gcc librdkafka-dev python3-dev

# upgrading pip solves many installation problems
RUN pip3 install --upgrade pip

WORKDIR /app

# leverage Docker cache
COPY requirements.lock ./
RUN PYTHONDONTWRITEBYTECODE=1 pip install --no-cache-dir -r requirements.lock

ARG VCS_REVISION
RUN echo "$VCS_REVISION" > ./version

COPY src .

CMD ["python3", "rkagent/main.py"]
