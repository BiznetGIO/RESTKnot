FROM alpine

RUN mkdir /app
COPY . /app
WORKDIR /app

RUN apk update && \
    apk --no-cache add python3 git && \
    pip3 install -r requirements.txt && \
    pip3 install gunicorn

EXPOSE 5000
