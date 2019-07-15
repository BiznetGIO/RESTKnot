FROM alpine
MAINTAINER Sofyan Saputra "sofyan@biznetgio.com"

RUN apk update && \
    mkdir /app
WORKDIR /app
COPY . /app

RUN apk update && \
    apk --no-cache add gcc linux-headers python3 python3-dev musl-dev libcap-dev libcap-ng-dev knot knot-libs knot-dev && \
    pip3 install --upgrade pip && \
    pip3 install gunicorn && \
    pip3 install -r requirements.txt

EXPOSE 6967
RUN apk del build-base