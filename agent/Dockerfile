FROM alpine
MAINTAINER Sofyan Saputra "sofyan@biznetgio.com"


RUN apk update && \
    mkdir /app && \
    apk --no-cache add gcc linux-headers python3 python3-dev musl-dev libcap-dev libcap-ng-dev knot knot-libs knot-dev make && \
    pip3 install --upgrade pip && \
    pip3 install domba

WORKDIR /app
COPY . /app


