FROM alpine

RUN mkdir /app
COPY . /app
WORKDIR /app

RUN apk update && \
    apk --no-cache add python3 python3-dev git && \
    pip3 install -r requirements.txt
