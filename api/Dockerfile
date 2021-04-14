FROM python:3.7-alpine

# working with timezones
RUN apk add tzdata

# need these depedencies in order for psycopg2 to be installed via pip
# Alpine can't use psycopg2-binary since it din't support manylinux
RUN apk add gcc linux-headers postgresql-dev musl-dev && \
    pip3 install gunicorn

WORKDIR /restknotapi

# leverage Docker cache
COPY ./requirements.txt /restknotapi/requirements.txt

COPY ./servers.example.yml /restknotapi/servers.yml

RUN pip3 install -r /restknotapi/requirements.txt

ARG BUILD_VERSION
RUN echo "$BUILD_VERSION" > build-version.txt

COPY . /restknotapi
# check build version
RUN cat /restknotapi/build-version.txt

RUN apk del gcc linux-headers musl-dev && \
    rm -rf /var/cache/apk/*

EXPOSE 5000
CMD ["gunicorn", "autoapp:app", "-b", "0.0.0.0:5000"]
