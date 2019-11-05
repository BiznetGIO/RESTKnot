FROM python:3.7-alpine

RUN mkdir /dnsagent
COPY . /dnsagent
WORKDIR /dnsagent

RUN pip3 install -r requirements.txt
RUN pip3 install -e .
