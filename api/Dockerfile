FROM python:3.11.3-slim-buster

ENV PIP_DEFAULT_TIMEOUT=100 \
  POETRY_VERSION=1.4 \
  GUNICORN_VERSION=20.1.0

RUN apt-get update
# working with timezones
RUN apt-get install --no-install-recommends --yes tzdata
# confluent-kafka-python needs these
RUN apt-get install --no-install-recommends --yes librdkafka-dev python3-dev
# psycopg2 needs these
RUN apt-get install --no-install-recommends --yes build-essential libpq-dev

# activate virtualenv
ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# upgrading pip solves many installation problems
RUN pip3 install --upgrade pip
RUN pip3 install "gunicorn==$GUNICORN_VERSION"
RUN pip3 install "poetry==$POETRY_VERSION"

WORKDIR /restknotapi

# leverage Docker cache
COPY poetry.lock pyproject.toml /restknotapi/

COPY ./config.example.yml /restknotapi/config.yml

RUN poetry install --only main --no-interaction --no-ansi

ARG VCS_REVISION
RUN echo "$VCS_REVISION" > version

COPY . /restknotapi
# check build version
RUN cat /restknotapi/version

EXPOSE 5000
CMD ["gunicorn", "autoapp:app", "-b", "0.0.0.0:5000"]
