FROM alpine
MAINTAINER Sofyan Saputra "sofyan@biznetgio.com"

RUN apk update
RUN apk --no-cache add build-base bash git openssl openssl-dev libxslt-dev linux-headers libffi-dev
RUN apk --no-cache add python3 python3-dev 
RUN pip3 install --upgrade pip
COPY requirements.txt /
RUN pip3 install -r /requirements.txt
RUN pip3 install gunicorn
WORKDIR /app
EXPOSE 6969
RUN apk del build-base