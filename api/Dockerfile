FROM python:3.7-alpine

# need these depedencies in order for psycopg2 to be installed via pip
# Alpine can't use psycopg2-binary since it din't support manylinux
RUN apk add gcc linux-headers postgresql-dev musl-dev && \
    pip3 install gunicorn

WORKDIR /restknotapi

# leverage Docker cache
COPY ./requirements.txt /restknotapi/requirements.txt

RUN pip3 install -r /restknotapi/requirements.txt
COPY . /restknotapi

EXPOSE 5000
CMD ["gunicorn", "autoapp:app", "-b", "0.0.0.0:5000", "-w", "4"]
