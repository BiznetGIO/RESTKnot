# didn't work with apline
FROM python:3.7-slim-buster

RUN apt-get update

# working with timezones
RUN apt-get install --no-install-recommends --yes tzdata
# confluent-kafka-python needs these
RUN apt-get install --no-install-recommends --yes librdkafka-dev python3-dev

# activate virtualenv
ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# upgrading pip solves many installation problems
RUN pip3 install --upgrade pip

WORKDIR /dnsagent

COPY ./requirements.txt /dnsagent/requirements.txt
RUN pip3 install -r /dnsagent/requirements.txt

ARG BUILD_VERSION
RUN echo "$BUILD_VERSION" > build-version.txt

COPY . /dnsagent

# check build version
RUN cat /dnsagent/build-version.txt

ENV PYTHONPATH "${PYTHONPATH}:/dnsagent"
CMD ["python3", "dnsagent/start.py"]
