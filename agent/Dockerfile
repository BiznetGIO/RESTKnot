# didn't work with apline
FROM python:3.7-slim-buster

RUN mkdir /dnsagent
COPY . /dnsagent
WORKDIR /dnsagent

RUN pip3 install -r requirements.txt
RUN pip3 install -e .
