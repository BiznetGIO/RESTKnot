FROM alpine
MAINTAINER Sofyan Saputra "sofyan@biznetgio.com"

RUN apk update && \
    mkdir /app
WORKDIR /app
COPY . /app

RUN apk update && \
    apk --no-cache add gcc linux-headers postgresql-dev musl-dev python3 python3-dev && \
    pip3 install --upgrade pip && \
    pip3 install -r requirements.txt

EXPOSE 5000
RUN apk del build-base