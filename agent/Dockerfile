# didn't work with apline
FROM python:3.7-slim-buster

# working with timezones
RUN apt-get install -y tzdata

WORKDIR /dnsagent

COPY ./requirements.txt /dnsagent/requirements.txt
RUN pip3 install -r /dnsagent/requirements.txt

COPY . /dnsagent
RUN pip3 install -e /dnsagent
