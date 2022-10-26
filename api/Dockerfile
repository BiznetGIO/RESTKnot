FROM python:3.7-slim-buster

ENV PIP_DEFAULT_TIMEOUT=100 \
  POETRY_VERSION=1.2.2 \
  GUNICORN_VERSION=20.1.0

RUN apt-get update
# working with timezones
RUN apt-get install --no-install-recommends --yes tzdata
# confluent-kafka-python needs these
RUN apt-get install --no-install-recommends --yes librdkafka-dev python3-dev
# psycopg2 needs these
RUN apt-get install --no-install-recommends --yes build-essential libpq-dev

# upgrading pip solves many installation problems
RUN pip3 install --upgrade pip
RUN pip3 install "gunicorn==$GUNICORN_VERSION"
RUN pip3 install "poetry==$POETRY_VERSION"

WORKDIR /restknotapi

# leverage Docker cache
COPY poetry.lock pyproject.toml /restknotapi/

COPY ./config.yml /restknotapi/config.yml

RUN poetry config virtualenvs.create false && poetry install --no-dev --no-interaction --no-ansi

ARG BUILD_VERSION
RUN echo "$BUILD_VERSION" > build-version.txt

COPY . /restknotapi
# check build version
RUN cat /restknotapi/build-version.txt

EXPOSE 5000
CMD ["gunicorn", "autoapp:app", "-b", "0.0.0.0:5000"]
