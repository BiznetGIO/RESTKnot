# didn't work with apline
FROM python:3.7-slim-buster

# working with timezones
RUN apt-get install -y tzdata

WORKDIR /dnsagent

COPY ./requirements.txt /dnsagent/requirements.txt
RUN pip3 install -r /dnsagent/requirements.txt

ARG BUILD_VERSION
RUN echo "$BUILD_VERSION" > build-version.txt

COPY . /dnsagent

# check build version
RUN cat /dnsagent/build-version.txt

RUN pip3 install -e /dnsagent
