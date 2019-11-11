FROM python:3.7-alpine

RUN mkdir /restknotapi
COPY . /restknotapi
WORKDIR /restknotapi

# need these depedencies in order for psycopg2 to be installed via pip
RUN apk --no-cache add gcc linux-headers postgresql-dev musl-dev && \
    pip3 install -r requirements.txt && \
    pip3 install gunicorn

EXPOSE 5000
CMD ["gunicorn", "autoapp:app", "-b", "0.0.0.0:5000"]
