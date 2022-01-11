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

ARG VCS_REVISION
RUN echo "$VCS_REVISION" > vcs_revision.txt

COPY . /dnsagent

# check build version
RUN cat /dnsagent/vcs_revision.txt

ENV PYTHONPATH "${PYTHONPATH}:/dnsagent"
CMD ["python3", "dnsagent/start.py"]
